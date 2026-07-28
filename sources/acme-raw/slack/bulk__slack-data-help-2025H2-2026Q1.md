---
title: "Slack archive — #data-help (+ #board-prep, #cs-at-risk, #revenue, #random) — 2025-H2 through 2026-Q1"
source_url: "internal://acme/slack/data-help/2025H2-2026Q1-archive"
license: "synthetic-demo"
attribution: "Synthetic Slack export, Acme Inc internal demo. Acme Inc is fictitious."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

> *(Multi-month export. #data-help is the primary channel; interleaved snippets from #board-prep, #cs-at-risk, #revenue, and #random are included where threads cross-referenced each other or were exported in the same window. Raw dump, light cleanup only — emoji codes, edits, joins/leaves, and side-replies preserved. Some DM references and customer PII redacted. Threads separated by blank lines.)*

---

# #random — 2025-07-01 — Q3 kickoff vibes

**sam.reyes** — 9:02 AM
happy july everyone :tada: Q3 is going to be a big one. Series B money is in the bank, let's go build

**jasmine.park** — 9:05 AM
:rocket::rocket:

**priya.anand** — 9:06 AM
can we get the 2nd floor AC fixed before "a big one" turns into "a sweaty one" :hot_face:

**facilities** — 9:20 AM
ticket's in. vendor coming thursday

**marco.silva** — 9:31 AM
unrelated but the SF office coffee machine is making a noise that can only be described as "dying robot". is that a facilities ticket or do we just accept it as ambiance now

**facilities** — 9:33 AM
that's the descaling light. someone needs to run a cleaning cycle, it's not broken

**marco.silva** — 9:34 AM
i nominate whoever drank the last cup (not me)

**olivia.tran** — 9:35 AM
it's always "not me" in this channel and yet the machine is always empty :thinking_face:

---

# #data-help — 2025-07-02 — where do active users live

**newgrad.sam** — 10:14 AM
hi team, first week on the data side :wave: dumb question — where do I find whether a user is "active"? is there a flag or do I compute it

**nina.patel** — 10:22 AM
welcome! there's a denorm `is_active` boolean on `dim_users`, but for any real analysis don't trust the flag — compute activity from events. "active in last 28d" = a user with at least one `fact_user_events` row in the trailing 28 days. the flag is a nightly rollup and lags.

**newgrad.sam** — 10:24 AM
got it. and where's the events table exactly

**nina.patel** — 10:25 AM
`nexus-analyst-demo.acme.fact_user_events`. flat dataset, everything hangs off `acme.` directly. don't go looking for `acme.marts.something`, there are no nested datasets here.

**newgrad.sam** — 10:26 AM
oh interesting, the dbt repo has like marts/cs and marts/finance folders so I assumed those were schemas

**rajiv.menon** — 10:31 AM
common trip-up. the dbt folder layout (`models/marts/finance`, `models/marts/cs`, etc) is **filesystem-only** — it's how we organize the SQL files, not where the tables land. every model materializes into the single flat `acme` dataset. so the file `models/marts/cs/account_health.sql` becomes the table `acme.account_health`, NOT `acme.marts.cs.account_health`.

**newgrad.sam** — 10:32 AM
ok that's a great thing to know on day 4, ty :pray:

**rajiv.menon** — 10:33 AM
pinned a note about it in this channel a while back. flat dataset, repeat after me :)

---

# #random — 2025-07-02 — lunch

**tom.becker** — 12:15 PM
lunch poll: poke on 2nd, the new ramen place, or sad desk salad :fork_and_knife:

**sarah.chen** — 12:16 PM
ramen but it's 85 degrees out, that feels aggressive

**tom.becker** — 12:16 PM
ramen is a year-round food, fight me

**yuki.sato** — 12:18 PM
poke. always poke.

**marco.silva** — 12:20 PM
i'm getting the ramen out of solidarity with tom's terrible judgment

**tom.becker** — 12:21 PM
i'll take it

---

# #data-help — 2025-07-08 — MRR vs ARR sanity

**lina.cho** — 11:40 AM
PSA since I keep getting DMed about this: for the **board-grade** ARR number, pull `acme.arr_snapshot`. it's a single-row mart (well, one row per snapshot_date) with `arr_usd` plus the per-tier breakdown `arr_pro_usd` / `arr_business_usd` / `arr_enterprise_usd` and `paying_customers`. do NOT re-derive ARR off `dim_customers.current_mrr_usd` — that denorm field drifts intraday.

**lina.cho** — 11:41 AM
if you want to understand the *definition*: ARR = SUM(mrr_usd) × 12 over `fact_subscriptions` where `is_current` AND `plan_tier != 'Free'`. arr_snapshot just bakes that so everyone reports the same number.

**dan.lee** — 11:48 AM
+1. the number of times "my ARR doesn't match the board deck" turns out to be "you summed the dim" is too high :sweat_smile:

**newgrad.sam** — 11:50 AM
noted. so current_mrr_usd on dim_customers is… what, just convenience?

**lina.cho** — 11:52 AM
denorm convenience for ad-hoc filtering ("show me UK customers on Pro right now"). marketing personalization uses it. fine for that. not for finance.

**newgrad.sam** — 11:53 AM
:saluting_face:

**rachel.stein** — 12:01 PM
can confirm arr_snapshot is what goes in the deck. it's ~$39M right now. if you see $42M somewhere it's a stale Looker thing, ignore it (more on that horror story another day)

**newgrad.sam** — 12:02 PM
$42M vs $39M is a big "another day" :eyes:

**rachel.stein** — 12:03 PM
oh it's a saga. later.

---

# #data-help — 2025-07-09 — the $42M Looker saga (resolved)

**jorge.martinez** — 2:30 PM
ok so re: rachel's teaser yesterday. the $42M ARR number that's been floating in a couple of Looker dashboards is **wrong**. it's a stale PDT (persistent derived table) that was caching a bad join from back in May. the real ARR is ~$39M per `acme.arr_snapshot`.

**jorge.martinez** — 2:31 PM
if your Looker tile says $42M, it's pulling the old PDT. we're rebuilding it. do not put $42M in front of anyone.

**rachel.stein** — 2:35 PM
this caused an actual minor heart attack when a sales deck and the board deck disagreed by $3M. turned out the board deck was right ($39M) and the Looker tile was the stale one.

**lina.cho** — 2:37 PM
the fix is: the PDT needs to read from `arr_snapshot` instead of re-summing a denormalized intermediate that double-counted some mid-cycle plan changes. jorge's rebuilding the LookML now.

**jorge.martinez** — 2:38 PM
yep. ETA end of week. until then: source of truth is `acme.arr_snapshot.arr_usd` = ~$39M (Business ~$32M, Enterprise ~$6M, Pro ~$1M, Free contributes $0).

**dan.lee** — 2:40 PM
adding "is your number from arr_snapshot or a Looker PDT?" to my mental checklist forever

**jasmine.park** — 2:45 PM
wait does this affect the marketing site "trusted by companies driving $XXM in automation" stat

**jasmine.park** — 2:45 PM
asking for a friend (the friend is me, the stat is on the homepage)

**jorge.martinez** — 2:47 PM
that stat is customer-reported value, totally different number, you're fine. this is just our internal ARR.

**jasmine.park** — 2:47 PM
phew

---

# #random — 2025-07-11 — weekend

**grace.liu** — 4:50 PM
weekend plans? i'm finally going to that pottery class i've been threatening to take for a year

**olivia.tran** — 4:52 PM
hiking if the smoke clears, otherwise couch + a very long book

**david.kim** — 4:55 PM
re-tiling my bathroom, which means by sunday i will hate grout

**grace.liu** — 4:56 PM
the grout arc. we've all been there.

**marco.silva** — 5:01 PM
i'm on call for #cs-at-risk this weekend so my "plans" are "hope nothing goes critical" :pray:

**elena.volkov** — 5:03 PM
the health-bot digest is 08:00 UTC, so you get one scary morning ping and then freedom. probably.

**marco.silva** — 5:04 PM
"probably" she says, ominously

---

# #data-help — 2025-07-15 — engaged customer definition

**newgrad.sam** — 9:30 AM
PM just asked me "how many engaged customers do we have" and I realized I don't actually know what "engaged" means here. is it a defined thing or vibes

**nina.patel** — 9:38 AM
defined thing. **engaged customer = ≥3 active users AND ≥10 successful workflow runs in the trailing 28 days.** both conditions. it's materialized as `account_health.is_engaged`.

**newgrad.sam** — 9:39 AM
both conditions, not either?

**nina.patel** — 9:39 AM
AND, not OR. you need both the people (≥3 active users) and the usage (≥10 successful runs) in the last 28d.

**rajiv.menon** — 9:44 AM
heads up that this definition was **recalibrated in Q4 2025** — the old definition was looser (lower thresholds) and overcounted. if you're comparing an engaged-count from an old doc to today's, they're not apples to apples. current canon is ≥3 active users AND ≥10 successful runs / trailing 28d.

**newgrad.sam** — 9:45 AM
ok so if someone shows me a "engaged customers" slide from like Q2 2025 I should treat it as a different metric

**rajiv.menon** — 9:46 AM
correct. footnote the date.

**dan.lee** — 9:50 AM
and "monitoring" in account_health basically means "not engaged" — it's the lukewarm bucket. engaged → healthier statuses, not engaged → monitoring (assuming nothing worse is flagged).

**newgrad.sam** — 9:51 AM
this channel is my onboarding doc at this point, thank you

---

# #data-help — 2025-07-18 — which table is canonical for account health

**marco.silva** — 1:14 PM
where's the canonical account health data? I see references to a few things in dbt and I want to make sure I'm querying the right table for my QBR prep

**dan.lee** — 1:20 PM
`acme.account_health`. one row per customer, has the status enum + the underlying signals (`is_engaged`, `utilization_band`, `has_open_p1_over_48h`, `has_recent_nps_detractor`, `has_uncollectible_recent`, `n_open_p1_over_48h`, `account_health_status`). that's the shipped mart, use it.

**marco.silva** — 1:21 PM
great. and is it acme.marts.cs.account_health? that's the path in the dbt repo

**dan.lee** — 1:22 PM
nope — flat. `acme.account_health`. the `marts/cs/` part is just the folder the .sql file lives in. bigquery here has no nested datasets. query `acme.account_health`.

**marco.silva** — 1:23 PM
:ok_hand: thx, querying the flat one

**olivia.tran** — 1:30 PM
piggybacking — is there a separate "value realization" table? i swear i saw a spec for a VRS thing with a champion-login-recency column and a vrs_band

**dan.lee** — 1:34 PM
ahh. the **Value Realization Score (VRS)** is a *parked draft spec*. `vrs_band` and `champion_login_recency` are NOT built — there's no table, no columns, nothing materialized. it was a proposal that got shelved. use `account_health` as the shipped proxy for "how's this account doing." don't query VRS, it doesn't exist.

**olivia.tran** — 1:35 PM
ok good, I was about to go hunting for a table that doesn't exist. account_health it is.

**elena.volkov** — 1:40 PM
yeah VRS is on the someday-maybe pile. account_health covers the at-risk signals we actually need for renewals today. if/when VRS ships it'll be additive, but for now: account_health.

**olivia.tran** — 1:41 PM
copy that :pray:

---

# #board-prep — 2025-07-22 — first board deck of H2

**rachel.stein** — 8:30 AM
starting the Q3 board deck skeleton. metrics I need locked: ARR, NRR, GRR, logo churn, net new logos, engaged %, pipeline coverage. @lina.cho @rajiv.menon can you each confirm the source tables so I don't re-litigate this in October

**lina.cho** — 8:45 AM
finance side:
- ARR → `acme.arr_snapshot.arr_usd` (~$39M)
- NRR → `acme.nrr_trailing_12.nrr` (~1.07)
- GRR → `acme.nrr_trailing_12.grr` (~0.94)
all flat tables. arr_snapshot is canonical, don't re-sum the dim.

**rajiv.menon** — 8:52 AM
product/usage side:
- engaged % → from `acme.account_health.is_engaged` (≥3 active users AND ≥10 successful runs / trailing 28d)
- workflow run health → `acme.workflow_runs_daily`
logo churn + net new logos I'd pull from `fact_subscriptions` change_type rows, happy to write the SQL.

**rachel.stein** — 8:55 AM
perfect. this is going in a pinned "board metric sources" note so we never argue about it again.

**sam.reyes** — 9:10 AM
+1000 to a pinned source-of-truth note. last quarter we burned an afternoon on the ARR discrepancy thing.

**rachel.stein** — 9:11 AM
the $42M ghost. never again.

---

# #random — 2025-07-25 — standup time poll

**priya.anand** — 8:00 AM
eng standup time poll because the 9:30 slot is colliding with too many calls. options: 9:00, 9:45, 10:15. react below :alarm_clock:

**david.kim** — 8:02 AM
:nine: (9:00, I'm a morning person and also smug about it)

**nina.patel** — 8:05 AM
9:45 please, 9:00 is a crime

**rajiv.menon** — 8:06 AM
10:15, let me have my coffee in peace

**priya.anand** — 8:30 AM
the spread on this poll tells me we will never agree on anything, love that for us. going 9:45 as the compromise.

**david.kim** — 8:31 AM
the morning people have lost. dark day.

---

# #data-help — 2025-07-29 — bookings, do not multiply by 12

**tom.becker** — 3:40 PM
quick one for the data crowd — I'm building a "Q3 bookings by channel" view and the numbers look way too big. like suspiciously big. am I doing something dumb

**lina.cho** — 3:48 PM
paste the query?

**tom.becker** — 3:50 PM
```sql
SELECT first_touch_channel, SUM(bookings_acv_usd) * 12 AS annual_bookings
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at >= '2025-07-01'
GROUP BY first_touch_channel;
```

**lina.cho** — 3:52 PM
there it is — drop the `* 12`. `bookings_acv_usd` is **already annualized** (it's annual contract value). multiplying by 12 gives you a number 12× too big. ACV is annual, MRR is monthly; you only ×12 when going from monthly to annual, and bookings are already annual.

**tom.becker** — 3:53 PM
OH. ok yeah that's the suspiciously-big. removing the ×12.

**lina.cho** — 3:54 PM
```sql
SELECT first_touch_channel, SUM(bookings_acv_usd) AS bookings_acv
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at >= '2025-07-01'
GROUP BY first_touch_channel
ORDER BY bookings_acv DESC;
```
that's your Q3 bookings by channel. group by `first_touch_channel`, no multiplier.

**tom.becker** — 3:55 PM
much more believable numbers now. thank you :pray:

**jorge.martinez** — 4:00 PM
this is like the #3 most common mistake in here. ACV is already annual. someone should tattoo it on the channel topic.

**lina.cho** — 4:01 PM
honestly tempted

---

# #data-help — 2025-08-04 — bookings_attribution scope (free→paid)

**nina.patel** — 10:10 AM
got a question forwarded from growth: "why don't our Free→Paid conversions show up in bookings?" — and it's a good question, want to make sure I answer it right

**lina.cho** — 10:18 AM
because `bookings_attribution` is **opportunity-sourced, AE-led deals only** (Closed_Won opportunities). Free→Paid self-serve conversions are product-led growth — there's no opportunity, no AE, so they do NOT appear in bookings_attribution. it's by design.

**nina.patel** — 10:20 AM
so where DO they show up

**lina.cho** — 10:23 AM
in `fact_subscriptions`. you detect a self-serve conversion as a customer who had a Free subscription row and then a paid row, linked via `changed_from_subscription_id`. that's the PLG funnel. bookings_attribution only sees the sales-led motion (Pro→Business and Business→Enterprise are AE-led, Free→Pro is self-serve).

**nina.patel** — 10:24 AM
got it. so if growth wants "PLG conversions" they need a fact_subscriptions query, not bookings. and if sales wants "bookings by channel" they group bookings_attribution by first_touch_channel.

**lina.cho** — 10:25 AM
exactly right. two different motions, two different tables.

**dan.lee** — 10:30 AM
worth noting Free ARR is $0 — Free is a non-paying tier. so a Free→Pro conversion is net-new paid ARR even though it never touched bookings_attribution. that trips people up when they try to reconcile "new ARR" with "bookings."

**nina.patel** — 10:31 AM
yeah that reconciliation is exactly what growth was trying to do. I'll explain the two motions. ty both.

---

# #cs-at-risk — 2025-08-06 — Enterprise critical rule reminder

**health-bot** — 8:00 AM
:rotating_light: 2 accounts moved to *critical* overnight. 3 *at_risk*. (daily 08:00 UTC digest)

**marco.silva** — 8:15 AM
on it. one of the criticals is an Enterprise — pulling the invoice history before I panic.

**elena.volkov** — 8:20 AM
good instinct. remember: **Enterprise critical is the uncollectible-invoice rule, NOT utilization.** Enterprise has unlimited seats so there's no utilization_band for them (it's NULL). an Ent only goes critical on a recent uncollectible invoice. low logins alone don't make an Ent critical.

**marco.silva** — 8:22 AM
confirmed, the Ent critical is a `has_uncollectible_recent = true`. that's a real billing problem, not a usage blip. escalating to finance.

**elena.volkov** — 8:24 AM
:+1: for non-Enterprise it's different — they go critical on uncollectible OR utilization_band < 0.20. but never apply the utilization rule to an Ent, you'll get false alarms.

**olivia.tran** — 8:30 AM
this is the thing I always have to re-explain to new CSMs. Enterprise = billing-driven critical only. wrote it on a sticky note on my monitor.

---

# #random — 2025-08-08 — coffee machine, again

**marco.silva** — 11:00 AM
the coffee machine descaling light is STILL on. it has been a month. someone please run the cycle. I will buy you a coffee. from a different machine. that works.

**facilities** — 11:30 AM
running it now. for the record the instructions are taped to the side of the machine.

**marco.silva** — 11:31 AM
"taped to the side of the machine" is facilities for "you could have done this yourself" and I respect the shade

**olivia.tran** — 11:33 AM
:joy::joy:

---

# #data-help — 2025-08-12 — NRR cohort: keep churned customers in

**lina.cho** — 2:00 PM
seeing a recurring bug in people's NRR attempts so dropping the canonical pattern here. our board NRR comes from `acme.nrr_trailing_12`. the model is **fixed-cohort, trailing 12 months**:
- cohort = customers who were **paid** (non-Free) as of `snapshot_date − 12 months`
- denominator = that cohort's MRR at the start (12mo ago)
- numerator = the SAME customer set's MRR today — **including churned customers at $0**

**lina.cho** — 2:01 PM
the critical bit: churned customers **stay in the cohort at $0 end MRR**. you do this with a LEFT JOIN from the cohort to current subscriptions and `COALESCE(end_mrr_usd, 0)`. if you use an INNER JOIN you silently DROP the churned customers, which **inflates NRR** because you've removed all the zeros from the numerator.

**newgrad.sam** — 2:05 PM
ohh. so an INNER JOIN would make NRR look better than reality

**lina.cho** — 2:06 PM
exactly — INNER JOIN = "survivorship bias" NRR. you'd be measuring retention only on the customers who didn't leave, which is meaningless. the churned ones contribute their original MRR to the denominator and $0 to the numerator. that's the whole point of NRR.

**rajiv.menon** — 2:10 PM
the model does it correctly: LEFT JOIN cohort → current state, COALESCE end MRR to 0. churned customers are present with end_mrr = 0. downgrades to Free also count as churn (Free is $0 paid revenue). we land at NRR ~1.07.

**newgrad.sam** — 2:12 PM
and GRR?

**rajiv.menon** — 2:14 PM
GRR caps the numerator at the denominator per-customer — no expansion credit. so expansions can't push it above 1.0; only churn and contraction pull it down. we're at GRR ~0.94. NRR ~1.07, GRR ~0.94, the gap is expansion.

**newgrad.sam** — 2:15 PM
that finally clicked. LEFT JOIN + COALESCE for the zeros. thank you.

**lina.cho** — 2:16 PM
the number of "my NRR is 1.3, is that good??" messages that turn out to be a sneaky INNER JOIN… :sweat_smile: it's always the inner join.

---

# #data-help — 2025-08-19 — Cobalt Systems run failures

**marco.silva** — 9:40 AM
Cobalt Systems (cust_000700) — their workflow runs have a bunch of failures this week and they're a Business account, 80 seats, that I do NOT want to lose. can someone help me see what's failing

**david.kim** — 9:48 AM
`acme.workflow_runs_daily` will give you the daily rollup with the error breakdown columns. for cust_000700:
```sql
SELECT run_date, n_runs, n_success, success_rate,
       auth_failed_count, rate_limited_count, step_timeout_count, integration_down_count
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE customer_id = 'cust_000700'
  AND run_date >= '2025-08-12'
ORDER BY run_date;
```

**marco.silva** — 9:55 AM
ran it — `auth_failed_count` is spiking, the others are flat. so it's auth, not us being down

**david.kim** — 9:57 AM
right, `AUTH_FAILED` means a connected integration's credentials expired or got revoked on the customer's side. that's usually "their Salesforce token expired" not an Acme outage. you can confirm by drilling into `fact_workflow_runs` with `error_code = 'AUTH_FAILED'` for that customer if you want the per-run detail.

**marco.silva** — 9:58 AM
that's a much friendlier conversation to have with them — "hey your token expired" vs "we broke." thank you, reaching out to their admin.

**olivia.tran** — 10:05 AM
this is why I love workflow_runs_daily for CSM prep. the error columns tell you whose fault it is before the call :sweat_smile:

---

# #random — 2025-08-20 — Amsterdam office

**yuki.sato** — 7:30 AM
greetings from the Amsterdam office :netherlands: the espresso machine here works flawlessly, just saying

**marco.silva** — 9:35 AM
i'm in SF and I felt that personally

**elena.volkov** — 9:36 AM
the EMEA office flexing on the coffee situation is a recurring theme and frankly deserved

**yuki.sato** — 9:40 AM
come visit, we have stroopwafels in the kitchen at all times

**sarah.chen** — 9:41 AM
booking a "customer visit" to Amsterdam immediately

---

# #data-help — 2025-08-26 — utilization_band and health statuses

**grace.liu** — 11:20 AM
can someone walk me through `account_health_status`? I have a Pro customer showing "critical" and I want to understand why before I reach out

**dan.lee** — 11:30 AM
the enum is: `critical / at_risk / monitoring / stable / healthy_expansion`. for a **non-Enterprise** account (Pro/Business), critical fires on either a recent uncollectible invoice OR `utilization_band < 0.20`. so your Pro critical is probably low utilization — they're paying for seats they're not using.

**grace.liu** — 11:32 AM
how's utilization_band defined

**dan.lee** — 11:34 AM
`utilization_band = active_users_28d / seat_count_licensed` for non-Enterprise. so if they licensed 20 seats but only 3 users are active in the last 28d, that's 0.15 → below the 0.20 critical threshold. for **Enterprise** it's NULL (unlimited seats, no utilization rule).

**grace.liu** — 11:36 AM
ahh so my Pro account licensed a bunch of seats and isn't using them. that's a "let's right-size your plan or drive adoption" conversation, not a "you're churning" conversation necessarily

**dan.lee** — 11:38 AM
exactly. and the other statuses: `at_risk` = open P1 ticket >48h OR a recent NPS detractor. `healthy_expansion` = engaged AND utilization ≥ 0.6 (they're using it heavily, expansion candidate). `stable` / `monitoring` are the in-betweens, monitoring being the not-engaged lukewarm bucket.

**grace.liu** — 11:40 AM
this is super helpful. so the status already encodes the "why" if I know the rules. ty!

**elena.volkov** — 11:45 AM
and to be safe — all of this is in `acme.account_health`, the flat table. not a VRS thing, not a nested path. account_health has everything you need.

---

# #board-prep — 2025-09-03 — Series B close, ARR check

**sam.reyes** — 8:00 AM
Series B is officially closed :tada: $80M total raised now. for the announcement I want our headline metrics double-checked. ARR?

**rachel.stein** — 8:15 AM
ARR ~$39M per `acme.arr_snapshot`. Business ~$32M, Enterprise ~$6M, Pro ~$1M. (Free is $0.) NRR ~1.07, GRR ~0.94. ~745 active customers of 800 total.

**sam.reyes** — 8:17 AM
perfect, those are the numbers I've been saying. good that they match the source of truth.

**marcus.webb** — 8:30 AM
sales context for the announcement: we're at ~520 paying customers, the rest is Free. Enterprise is small in logo count (~5% of paying) but punches above weight in ARR.

**rachel.stein** — 8:32 AM
right — Enterprise is ~$6M ARR on a handful of logos, that's the leverage. Business is the bulk at ~$32M.

**sam.reyes** — 8:35 AM
love it. let's announce. great quarter team :rocket:

---

# #data-help — 2025-09-08 — Marigold Health seat utilization confusion

**olivia.tran** — 10:00 AM
quick check on Marigold Health (cust_000701) — they're Enterprise, 300 seats, and my QBR template wants a "seat utilization %" but the account_health row shows utilization_band as NULL. is that a bug?

**dan.lee** — 10:08 AM
not a bug — `utilization_band` is **NULL for all Enterprise accounts** by design. Enterprise plans are unlimited seats, so "active users / licensed seats" doesn't mean anything useful for them. the 300 "seats" is more of a contractual/pricing artifact than a hard cap.

**olivia.tran** — 10:10 AM
ahh. so for an Enterprise QBR I shouldn't show a utilization % at all

**dan.lee** — 10:12 AM
right. show them raw adoption instead: active users (count), workflow run volume, success rate. those are meaningful. utilization-as-a-ratio is a non-Enterprise concept. and remember Enterprise critical is purely the uncollectible-invoice rule, so utilization being NULL doesn't affect their health status.

**olivia.tran** — 10:14 AM
got it. Marigold is healthy on adoption anyway, they're a partner-sourced account that's been growing. I'll show absolute usage numbers. ty!

**elena.volkov** — 10:20 AM
+1, and Marigold's CSM-led growth story is a good one for the QBR. lean into the adoption trend, skip the utilization ratio.

---

# #revenue — 2025-09-10 — Q3 bookings pacing

**marcus.webb** — 9:00 AM
how are we pacing on Q3 bookings? @tom.becker @sarah.chen the dashboard says we're behind but I want to make sure the dashboard is right this time (looking at you, $42M ghost)

**lina.cho** — 9:15 AM
bookings pacing is from `acme.bookings_attribution` summing `bookings_acv_usd` (already annual, no ×12) for opps with `closed_won_at` in Q3. let me pull it.

**lina.cho** — 9:22 AM
```sql
SELECT DATE_TRUNC(closed_won_at, MONTH) AS mo, SUM(bookings_acv_usd) AS bookings
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at BETWEEN '2025-07-01' AND '2025-09-30'
GROUP BY mo ORDER BY mo;
```
numbers look real (no ×12 inflation). we're behind on the month but September has a few Enterprise deals in late-stage that should close.

**marcus.webb** — 9:25 AM
which Enterprise deals

**sarah.chen** — 9:30 AM
Quartz Foundry (cust_000714) is in final procurement, Marigold expansion is in legal. both partner-sourced.

**marcus.webb** — 9:32 AM
ok those are real. and remember bookings_attribution only has the AE-led stuff — the PLG Free→Paid conversions aren't in here, those are gravy on top in the subscriptions data.

**lina.cho** — 9:33 AM
correct, PLG conversions never touch bookings_attribution. that's a fact_subscriptions thing.

**marcus.webb** — 9:34 AM
right right. ok feeling better about pacing. close those Ent deals folks :muscle:

---

# #random — 2025-09-12 — friday

**david.kim** — 4:45 PM
the grout from july has been fully avenged, bathroom is done, I am a changed man

**grace.liu** — 4:47 PM
the grout arc reaches its conclusion. moving and beautiful.

**david.kim** — 4:48 PM
next: regrouting my entire personality

**priya.anand** — 4:50 PM
this is the content I subscribe to #random for

---

# #data-help — 2025-09-16 — paused accounts in counts

**newgrad.sam** — 1:30 PM
when I count "active customers" — what do I do with paused accounts? we have like 10 paused. are they active or churned?

**lina.cho** — 1:40 PM
neither, technically. `status` on `dim_customers` is one of {active, paused, churned}. paused = temporarily suspended (often a billing hold or a "we're reorganizing, pause us for a quarter"), not churned but not actively paying right now. for most metrics I exclude paused from "active" but DON'T count them as churned either.

**newgrad.sam** — 1:42 PM
so the breakdown is roughly: 800 total, ~745 active, ~45 churned, ~10 paused

**lina.cho** — 1:43 PM
yep that's the rough split. for ARR purposes a paused account's subscription typically isn't `is_current` so it falls out of the ARR sum anyway. for logo counts, be explicit about whether you're including paused.

**marco.silva** — 1:50 PM
Tamarind Group (cust_000706) is one of our paused ones — Business, 55 seats, they paused in Jan— wait no, they'll pause in January. right now they're active. nvm, ignore me, I'm thinking of a future thing.

**marco.silva** — 1:51 PM
(disregard, brain glitch, Tamarind is active as of now)

**lina.cho** — 1:52 PM
lol the "thinking of a future thing" brain glitch. anyway yes, be explicit about paused in any logo count.

**newgrad.sam** — 1:53 PM
will do. ty!

---

# #cs-at-risk — 2025-09-22 — at_risk signals

**health-bot** — 8:00 AM
:rotating_light: 1 account moved to *critical*. 5 *at_risk*. (daily 08:00 UTC digest)

**grace.liu** — 8:20 AM
5 at_risk is a lot for a monday. what's the breakdown — is it P1 tickets or NPS detractors?

**olivia.tran** — 8:25 AM
`at_risk` fires on `has_open_p1_over_48h = true` OR `has_recent_nps_detractor = true`. pull the account_health rows and check which flag is set:
```sql
SELECT customer_id, has_open_p1_over_48h, n_open_p1_over_48h, has_recent_nps_detractor
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_health_status = 'at_risk';
```

**grace.liu** — 8:32 AM
ran it — 3 are P1-over-48h, 2 are NPS detractors. so 3 are "we have an unresolved fire" and 2 are "someone's unhappy on a survey."

**olivia.tran** — 8:34 AM
right, different playbooks. the P1s are support escalations — loop in whoever owns the ticket (`assigned_to_employee_id` on `fact_support_tickets`). the detractors are relationship — that's a CSM outreach.

**grace.liu** — 8:35 AM
on it. and only P1 escalates to this signal right? not P2

**olivia.tran** — 8:36 AM
correct, `has_open_p1_over_48h` is P1-priority tickets open more than 48 hours. P2 and below don't trip the at_risk flag.

**elena.volkov** — 8:40 AM
nice triage. remember the two NPS detractors might also just be having a bad week — check if it's a champion or a random user before you escalate to a save play.

---

# #data-help — 2025-09-25 — where are support tickets

**newgrad.sam** — 11:00 AM
where do support tickets live and what's the grain

**nina.patel** — 11:08 AM
`acme.fact_support_tickets`. one row per ticket. key columns: `opened_at`, `closed_at`, `channel`, `priority` (P1/P2/P3/etc), `category`, `resolution_time_hours`, `csat_score`, `assigned_to_employee_id`. customer + user FKs too.

**newgrad.sam** — 11:10 AM
and CSAT is per-ticket?

**nina.patel** — 11:11 AM
per-ticket CSAT (post-resolution survey), separate from NPS. NPS is in `fact_nps_responses` (relationship survey, quarterly-ish, has `score` 0-10 and `segment`). don't confuse the two — CSAT = "how was this ticket", NPS = "how do you feel about us overall."

**newgrad.sam** — 11:13 AM
got it. two different satisfaction signals, two tables.

**nina.patel** — 11:14 AM
exactly. and account_health's `has_recent_nps_detractor` reads from the NPS table (detractor = score 0-6), not from CSAT.

**newgrad.sam** — 11:15 AM
:brain: ty

---

# #random — 2025-09-26 — office dog

**sam.reyes** — 2:00 PM
office dog 🐕 is in today. she's on the 2nd floor charming everyone and contributing nothing to the roadmap, a role model honestly

**lina.cho** — 2:01 PM
brb relocating my standing desk to the 2nd floor permanently

**grace.liu** — 2:02 PM
the only acceptable reason to leave my desk

**david.kim** — 2:05 PM
productivity will dip 40% for the next hour and it's worth it

---

# #board-prep — 2025-09-30 — Q3 close numbers

**rachel.stein** — 4:00 PM
Q3 books are closing. final-ish numbers for the board update:
- ARR ~$39M (arr_snapshot)
- NRR ~1.07, GRR ~0.94 (nrr_trailing_12)
- logo count ~800 total, ~745 active
- Q3 bookings (AE-led, from bookings_attribution, no ×12) coming from marcus's team

**marcus.webb** — 4:15 PM
Q3 AE-led bookings landing roughly on plan after the late Enterprise closes. Quartz Foundry closed-won, Marigold expansion closed. I'll send the channel breakdown — partner and outbound are our top two channels this quarter.

**rachel.stein** — 4:18 PM
partner + outbound on top, makes sense given the Enterprise mix. send me the bookings_attribution grouped by first_touch_channel when you have it.

**marcus.webb** — 4:20 PM
on it. (no ×12, I learned my lesson :sweat_smile:)

**rachel.stein** — 4:21 PM
:joy: the channel topic tattoo worked

---

# #data-help — 2025-10-06 — churn definition, downgrades to Free

**newgrad.sam** — 9:50 AM
how do I count churned customers correctly? do I just count `status = 'churned'` on dim_customers or is there more nuance

**rajiv.menon** — 10:00 AM
for a quick logo count `status = 'churned'` on dim is fine, but remember dim is a nightly denorm so it lags. for revenue churn (and for the NRR cohort) the authoritative signal is a `change_type = 'churn'` row in `fact_subscriptions`. and importantly: **a downgrade to Free counts as churn** for revenue purposes, because Free is $0 paid revenue.

**newgrad.sam** — 10:02 AM
wait so if a Business customer downgrades all the way to Free, that's churn even though they technically still have an account?

**rajiv.menon** — 10:04 AM
for *revenue* retention, yes — they went from paying to $0, that's lost revenue. their logo is still "alive" (status might be active on Free) but for NRR/GRR they contribute $0 end MRR, same as a hard churn. that's why the NRR cohort uses LEFT JOIN + COALESCE to 0 — a downgrade-to-Free lands as a 0, not a missing row.

**newgrad.sam** — 10:06 AM
ok so "logo churn" and "revenue churn" can disagree because of Free downgrades

**rajiv.menon** — 10:07 AM
exactly. logo churn = they left entirely (status churned). revenue churn / the NRR zero = they stopped paying (hard churn OR downgrade to Free). be explicit about which one you're reporting.

**lina.cho** — 10:12 AM
this distinction has bitten every analyst here at least once. "why is my revenue retention worse than my logo retention" → Free downgrades.

**newgrad.sam** — 10:13 AM
adding to my growing personal glossary. ty both :pray:

---

# #cs-at-risk — 2025-10-09 — Verdant Cloud low engagement

**health-bot** — 8:00 AM
:rotating_light: 0 critical. 4 *at_risk*. 1 newly *monitoring* (dropped out of engaged). (daily 08:00 UTC digest)

**olivia.tran** — 8:30 AM
the "dropped out of engaged" one — is that Verdant Cloud (cust_000707)? they're Enterprise, APAC, ecommerce, and I've had a feeling their usage was sliding.

**elena.volkov** — 8:35 AM
let me check. yes, cust_000707 flipped from engaged → monitoring. they dipped below the engagement bar in the trailing 28d window.

**olivia.tran** — 8:37 AM
remind me of the exact bar again, I want to know how far off they are

**elena.volkov** — 8:38 AM
**engaged = ≥3 active users AND ≥10 successful runs / trailing 28d.** so they either dropped below 3 active users or below 10 successful runs (or both) in the last 28 days. pull their `workflow_runs_daily` and `fact_user_events` to see which.

**olivia.tran** — 8:45 AM
checked — they're still got plenty of active users but their successful run count cratered. looks like a workflow broke and they didn't fix it, so successful runs dropped under 10/28d.

**elena.volkov** — 8:47 AM
classic. the people are still there but the value (runs) stopped. that's a great proactive-outreach trigger — "hey we noticed your runs dropped, can we help unblock?" before it becomes a renewal problem. note they're Enterprise so this is monitoring/engagement, not a critical (Ent critical is billing-only).

**olivia.tran** — 8:48 AM
on it. reaching out to their champion. ty!

---

# #random — 2025-10-10 — pumpkin spice discourse

**grace.liu** — 11:00 AM
it's october, the pumpkin spice has returned, I will hear no slander

**tom.becker** — 11:01 AM
pumpkin spice is a scam invented by big latte

**grace.liu** — 11:02 AM
"big latte" I'm screaming

**yuki.sato** — 11:05 AM
in Amsterdam we have speculaas which is objectively superior, this debate is beneath me

**marco.silva** — 11:06 AM
the EMEA office superiority complex strikes again

**yuki.sato** — 11:07 AM
it's not a complex if it's true :innocent:

---

# #data-help — 2025-10-14 — pipeline / opportunities table

**tom.becker** — 1:00 PM
where do open opportunities live vs closed-won? I want a pipeline coverage number for the forecast call

**lina.cho** — 1:10 PM
`acme.fact_opportunities` has everything — open and closed. `stage` tells you where it is, `amount_usd` is the deal size, `close_date` is expected close, `closed_won_at` is populated when it's won, `loss_reason` when it's lost. for pipeline coverage you want open pipeline (not closed) divided by the quota/target for the period.

**tom.becker** — 1:12 PM
so closed-won opps are in fact_opportunities AND they flow into bookings_attribution?

**lina.cho** — 1:14 PM
right — `bookings_attribution` is the *closed-won subset* enriched with `bookings_acv_usd` (already annual!) and `first_touch_channel`. fact_opportunities is the full pipeline including open and lost. think of bookings_attribution as "the deals that actually closed-won, attributed."

**tom.becker** — 1:16 PM
got it. open pipeline from fact_opportunities (stage not closed), bookings from bookings_attribution. and no ×12 on the acv, yes I remember :sweat_smile:

**lina.cho** — 1:17 PM
:joy: you've earned your stripes. correct.

**marcus.webb** — 1:30 PM
chiming in — for the forecast call specifically I care about open pipeline by stage and the weighted forecast. tom can you pull fact_opportunities grouped by stage with the amount sums?

**tom.becker** — 1:32 PM
yep, on it.

---

# #data-help — 2025-10-20 — Onyx Robotics expansion, ACV math

**sarah.chen** — 10:00 AM
Onyx Robotics (cust_000704) wants to expand. they're Enterprise, currently $35K MRR. if I want to model a 20% expansion what's the right way to think about ACV vs MRR for the proposal

**lina.cho** — 10:10 AM
Onyx at $35K MRR = $420K ACV (×12). for an Enterprise deal you'll quote ACV (annual). a 20% expansion = $504K ACV = $42K MRR. when it closes-won it'll show in `bookings_attribution` with `bookings_acv_usd` of the *expansion* amount (already annual — don't ×12 it again, that's the whole point).

**sarah.chen** — 10:12 AM
right so the bookings_acv_usd I'd see for the expansion deal is the annual expansion value directly. and Onyx's mrr_usd in fact_subscriptions is the acv/12.

**lina.cho** — 10:13 AM
exactly. Enterprise `mrr_usd` rows are always `acv / 12`, so the ×12 to get ARR "just works" and you never multiply ACV by 12. Onyx is one of our bigger logos, nice expansion to chase.

**sarah.chen** — 10:14 AM
$420K → $504K ACV. great, modeling it. ty!

**marcus.webb** — 10:20 AM
love an Onyx expansion. that's tom's account originally but sarah's running the expansion? just making sure I have the right AE for the forecast.

**sarah.chen** — 10:22 AM
Onyx's AE of record is tom.becker, I'm just helping model it since I had the bandwidth. forecast credit to tom.

**marcus.webb** — 10:23 AM
:+1: good, just keeping the attribution clean.

---

# #board-prep — 2025-10-22 — Q3 board deck final review

**rachel.stein** — 8:00 AM
Q3 board deck is in final review. metric page locked:
- ARR ~$39M (arr_snapshot, NOT the $42M Looker ghost — that's fixed now)
- NRR ~1.07 / GRR ~0.94 (nrr_trailing_12, fixed cohort, churned-stay-in-at-$0)
- ~745 active logos / 800 total
- engaged % computed from account_health.is_engaged (recalibrated Q4 definition: ≥3 users + ≥10 runs / 28d)

wait — should I use the old or new engaged definition for the Q3 number? we recalibrated mid-quarter.

**rajiv.menon** — 8:15 AM
use the **new** (recalibrated) definition consistently — ≥3 active users AND ≥10 successful runs / trailing 28d. I re-ran the whole trailing series on the new definition so the trend is apples-to-apples. if you show the old looser number it'll look like engagement "dropped" when really we just tightened the ruler.

**rachel.stein** — 8:17 AM
perfect, that's the footnote I needed: "engaged-customer definition recalibrated in Q4 2025; trend restated on the new definition." using the restated series.

**sam.reyes** — 8:30 AM
good catch. a metric definition change mid-series is exactly the kind of thing that generates a board question. footnote it and we're clean.

**rachel.stein** — 8:31 AM
footnoted. deck's done. :tada:

---

# #random — 2025-10-24 — friday plans

**david.kim** — 4:30 PM
weekend: absolutely nothing, by design

**nina.patel** — 4:32 PM
aspirational. I have a wedding, which is just standing up in uncomfortable shoes

**grace.liu** — 4:33 PM
pottery class graduation, I made a bowl that is technically a bowl

**olivia.tran** — 4:35 PM
"technically a bowl" is the highest praise for early pottery, congrats

**david.kim** — 4:36 PM
my bathroom grout salutes your bowl

**grace.liu** — 4:37 PM
the lore of this channel is unmatched

---

# #data-help — 2025-10-28 — Sable Analytics NPS detractor

**marco.silva** — 2:00 PM
Sable Analytics (cust_000710) — Business, 90 seats, EMEA fintech — just popped as at_risk with a recent NPS detractor. how do I find the actual comment so I know what's wrong before I call?

**nina.patel** — 2:08 PM
`fact_nps_responses` has the `comment` field. filter:
```sql
SELECT responded_at, score, comment, segment, survey_quarter
FROM `nexus-analyst-demo.acme.fact_nps_responses`
WHERE customer_id = 'cust_000710'
ORDER BY responded_at DESC
LIMIT 5;
```
detractor = score 0-6. the comment should tell you the why.

**marco.silva** — 2:12 PM
got it — score of 4, comment is about a specific integration being flaky. so it's a product gripe, not a relationship problem. that's actionable.

**nina.patel** — 2:14 PM
nice. and that detractor is what's driving the `has_recent_nps_detractor = true` → at_risk status in account_health. once you address it and they re-survey better, the flag clears on the next refresh.

**marco.silva** — 2:15 PM
perfect. Sable's a good account otherwise, partner-sourced, healthy usage. I'll get their integration issue to support. ty!

**elena.volkov** — 2:20 PM
+1 — a single detractor on an otherwise-healthy account is usually a fixable product papercut, not a churn signal. good to address fast though.

---

# #revenue — 2025-10-30 — channel attribution question

**jasmine.park** — 11:00 AM
marketing question — when I look at `bookings_attribution.first_touch_channel`, that's the FIRST marketing touch that eventually led to the closed-won deal, right? not the last touch?

**lina.cho** — 11:10 AM
correct, `first_touch_channel` = the first attributed touch in the journey. so a deal that started from a `content` touch and later got an `outbound` follow-up would attribute to `content` as first-touch. it's one of {organic, paid_search, outbound, content, referral, partner, event, inbound}.

**jasmine.park** — 11:12 AM
ok so for "which channel sources our bookings" I group bookings_attribution by first_touch_channel and sum bookings_acv_usd

**lina.cho** — 11:13 AM
exactly that. (no ×12, it's annual.) if you want the full multi-touch journey there's `fact_marketing_touches` with every touch, but for the headline "bookings by channel" the first_touch on bookings_attribution is the standard view.

**jasmine.park** — 11:15 AM
and the PLG conversions aren't in there so the channel mix is purely sales-led, good to caveat that

**lina.cho** — 11:16 AM
yes — bookings_attribution is AE-led closed-won only, no Free→Paid self-serve. so "bookings by channel" is the sales-sourced picture. ty for caveating, that's the kind of thing that confuses execs otherwise.

**jasmine.park** — 11:17 AM
the more I learn about this data model the more I respect how many footguns there are :sweat_smile: ty

---

# #data-help — 2025-11-03 — the marts.cs path mistake (corrected)

**newgrad.sam** — 9:00 AM
ok I think I finally have a working account-health query but I keep getting a "Not found: Dataset" error. here's what I'm running:
```sql
SELECT customer_id, account_health_status
FROM `nexus-analyst-demo.acme.marts.cs.account_health`
WHERE account_health_status = 'critical';
```

**rajiv.menon** — 9:06 AM
ahh yeah that'll never work. there's no `acme.marts.cs` dataset. the dataset is **flat** — it's just `acme.account_health`. drop the `marts.cs`:
```sql
SELECT customer_id, account_health_status
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_health_status = 'critical';
```

**newgrad.sam** — 9:08 AM
oh my god it was the marts.cs the whole time. the dbt folder really got in my head.

**rajiv.menon** — 9:10 AM
it gets everyone. the `models/marts/cs/account_health.sql` path is where the SQL file lives in the repo — it has nothing to do with the BigQuery table path. all ~13 tables land flat in `acme.`. there are no nested datasets here, full stop.

**newgrad.sam** — 9:11 AM
works now. I'm going to write "ACME IS FLAT" on a sticky note.

**rajiv.menon** — 9:12 AM
join the sticky-note club, it's most of this channel :sweat_smile:

**david.kim** — 9:20 AM
for what it's worth I've argued we should rename the dbt folders to not look like schema paths but it's a big refactor nobody wants to own. so: the folders stay, the trip-up stays, the sticky notes multiply.

---

# #cs-at-risk — 2025-11-05 — Kestrel Networks budget churn

**marco.silva** — 10:00 AM
heads up team — Kestrel Networks (cust_000708) is churning. Business, 70 seats, NA-West devtools, was $10,430 MRR. it's a **budget cut** on their side, not a product problem. they're being forced to consolidate tooling after their own funding got tight. tom and I did everything we could.

**elena.volkov** — 10:08 AM
ugh, sorry marco. budget-driven churn is the worst kind because there's nothing to fix on our end. was their usage/health actually fine up to now?

**marco.silva** — 10:10 AM
yeah that's what stings — their account_health was stable, engagement was fine (well above the ≥3 users / ≥10 runs bar), no NPS detractors, no P1s. purely a "we lost our budget" story. churn_date will be this month.

**elena.volkov** — 10:12 AM
let's make sure we tag the churn reason correctly so it doesn't get miscounted as a product/dissatisfaction churn in the churn analysis. budget churn is a different bucket for the board narrative.

**marco.silva** — 10:14 AM
already flagged it. they said the door's open to come back when budget recovers, so I'm keeping the relationship warm. logging it as budget churn, not product.

**elena.volkov** — 10:15 AM
good. and for the NRR cohort math — Kestrel will sit in whatever cohort they belong to at $0 end MRR (LEFT JOIN keeps them in). that's correct, a churn is a churn for retention regardless of reason. the *reason* tagging is for the qualitative narrative, not the NRR number.

**marco.silva** — 10:17 AM
right. number-wise they're a zero. story-wise they're "budget, not us." both true.

**lina.cho** — 10:20 AM
exactly the right framing. and Kestrel at $10,430 MRR leaving will show as ~$125K of churned ARR in the cohort. it'll pull GRR down a touch but that's reality.

---

# #random — 2025-11-07 — daylight savings

**priya.anand** — 8:30 AM
reminder daylight savings this weekend, your standup-time poll trauma is about to get worse

**david.kim** — 8:31 AM
the 9:45 compromise is about to feel like 8:45 to my body, I'm furious in advance

**nina.patel** — 8:33 AM
the EMEA/US time difference shifts this week too so the cross-office calls are going to be chaos for a few days

**yuki.sato** — 8:40 AM
from Amsterdam: we already switched, your move America

**marco.silva** — 8:41 AM
the smugness from across the Atlantic is palpable

---

# #data-help — 2025-11-10 — Yarrow Logistics run volume

**marco.silva** — 11:00 AM
Yarrow Logistics (cust_000703) QBR coming up — Business, 120 seats, APAC logistics. I want their run-volume trend and success rate over the last quarter. best query?

**david.kim** — 11:10 AM
```sql
SELECT DATE_TRUNC(run_date, MONTH) AS mo,
       SUM(n_runs) AS runs, SUM(n_success) AS successes,
       SAFE_DIVIDE(SUM(n_success), SUM(n_runs)) AS success_rate
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE customer_id = 'cust_000703'
  AND run_date >= '2025-08-01'
GROUP BY mo ORDER BY mo;
```
that gives you monthly run volume + blended success rate. workflow_runs_daily is pre-aggregated daily so this is cheap.

**marco.silva** — 11:14 AM
ran it — they're a heavy user, run volume climbing, success rate ~97%. that's a great QBR story for a logistics account, they're clearly getting value.

**david.kim** — 11:16 AM
nice. if you want to show the "what could go wrong" angle, the error breakdown columns (auth_failed/rate_limited/step_timeout/integration_down) on the same table tell you what their failure modes are. but 97% success is a healthy account.

**marco.silva** — 11:17 AM
Yarrow's engaged and stable, this is a happy QBR for once. ty!

**olivia.tran** — 11:20 AM
a happy QBR, what a concept. enjoy it marco, the criticals will be back monday :joy:

---

# #data-help — 2025-11-14 — reconciling paying customer count

**lina.cho** — 1:00 PM
finance reconciliation flag: `arr_snapshot.paying_customers` and a hand-count of paid customers from dim_customers are off by a few. before anyone panics — this is the usual dim-lag thing. arr_snapshot is built off `fact_subscriptions` (is_current, non-Free); dim's `current_plan_tier` is a nightly denorm that lags. trust arr_snapshot's `paying_customers` for the board, not a dim hand-count.

**newgrad.sam** — 1:05 PM
so the canonical paying-customer count is arr_snapshot.paying_customers

**lina.cho** — 1:06 PM
for board reporting, yes. it's computed the same way as ARR (distinct customers with an is_current non-Free subscription). a dim hand-count will be close but can be off by a handful due to same-day plan changes the dim hasn't picked up.

**newgrad.sam** — 1:08 PM
got it. fact-based for board, dim for convenience/filtering. (this is the same lesson as ARR and the count-mismatch thread, I'm sensing a pattern)

**lina.cho** — 1:09 PM
:joy: you've found the unifying theory of this channel. **fact_subscriptions / the marts are canonical; dim_customers denorm fields are convenience and lag.** that's like 40% of the questions here.

**dan.lee** — 1:12 PM
the other 60% is "is the dataset nested" (no) and "do I ×12 the ACV" (no). truly we could replace half this channel with a bot.

**newgrad.sam** — 1:13 PM
please don't, where else would I learn about david's grout

---

# #random — 2025-11-18 — thanksgiving plans

**grace.liu** — 3:00 PM
thanksgiving plans? I'm hosting which means I'm stress-cooking for 12 people

**olivia.tran** — 3:02 PM
12 people is a lot of pottery, I mean plates, I mean — grace has me thinking in bowls now

**grace.liu** — 3:03 PM
I will bring one (1) handmade bowl to the dinner and it will hold exactly one thing poorly

**tom.becker** — 3:05 PM
I'm doing a "friendsgiving" which is just thanksgiving with worse table manners

**yuki.sato** — 3:10 PM
no thanksgiving in NL so I'll be working while you all eat, please think of me

**marco.silva** — 3:11 PM
we will think of you between the turkey and the nap

---

# #board-prep — 2025-11-20 — pre-read on retention narrative

**sam.reyes** — 9:00 AM
prepping the retention narrative for the next board meeting. I want to make sure I can defend NRR ~1.07 and GRR ~0.94 if pushed. @lina.cho can you give me the one-paragraph "how it's computed" so I'm not caught flat?

**lina.cho** — 9:15 AM
here's the defensible version:
"NRR is computed on a **fixed cohort over a trailing 12-month window**. The cohort is all paid (non-Free) customers as of 12 months ago. The denominator is that cohort's MRR at the start of the window; the numerator is the same customers' MRR today — **including any who churned or downgraded, counted at $0**. We use a LEFT JOIN so churned customers remain in the cohort at $0 rather than being dropped (dropping them would inflate NRR). NRR ~1.07. GRR uses the same cohort but caps each customer's contribution at their starting MRR (no expansion credit), so it isolates churn and contraction: GRR ~0.94. The ~13-point gap between them is expansion."

**sam.reyes** — 9:18 AM
that's exactly what I need. the "we don't drop churned customers, that would inflate it" line is the thing a sharp board member will probe and now I have the answer.

**lina.cho** — 9:20 AM
yep. the honest cohort math is our friend here — 1.07 NRR is real, not survivorship-inflated. if anyone re-derives with an INNER JOIN they'll get a higher number and we'll look conservative, which is fine.

**sam.reyes** — 9:22 AM
conservative-but-correct is exactly the posture I want with the board. thank you, this is great.

**rachel.stein** — 9:30 AM
+1, and the SQL is in the appendix (`nrr_trailing_12.sql`) if they want to audit. we've got this.

---

# #data-help — 2025-12-02 — VRS hunt (parked draft, corrected)

**dan.lee** — 10:00 AM
heads up, getting questions again about a "Value Realization Score." someone found an old Notion spec and started building a query against `vrs_band` and `champion_login_recency`. those columns **do not exist**. please don't.

**grace.liu** — 10:05 AM
oh I think that someone might be me, I saw the spec and got excited. so VRS isn't real?

**dan.lee** — 10:08 AM
the **VRS is a parked draft spec** — it was a proposal for a composite "is this customer realizing value" score with bands and a champion-login-recency input. it never got built. there's no `vrs_band` column, no `champion_login_recency` column, no VRS table anywhere in `acme.`. it's vaporware (well, draft-ware).

**grace.liu** — 10:10 AM
so what do I use instead for "is this account healthy / realizing value"

**dan.lee** — 10:12 AM
`acme.account_health` is the shipped proxy. it has the at-risk signals, engagement flag, utilization band, and the status enum. that's what we actually use for renewals and CSM triage today. VRS, if it ever ships, would be additive — but for now account_health is the answer.

**elena.volkov** — 10:15 AM
yeah I was in the room when VRS got parked. it was a good idea that needed champion-tracking data we don't reliably have. account_health covers the practical at-risk needs without it. so: account_health = real and shipped, VRS = parked draft, don't query it.

**grace.liu** — 10:16 AM
ok cool, redirecting to account_health. removing my doomed vrs_band query. ty for saving me an afternoon.

**dan.lee** — 10:18 AM
this is the second or third time VRS has lured someone in. I should put a tombstone in the Notion spec: "PARKED — use account_health." maybe that'll stop the hunts.

**elena.volkov** — 10:19 AM
please do, the VRS siren song claims an analyst a quarter :joy:

---

# #random — 2025-12-04 — holiday party logistics

**people-ops-bot** — 9:00 AM
:tada: holiday party is Dec 18, 6pm, the usual venue. RSVP by the 12th. plus-ones welcome. there will be a photo booth and questionable dancing.

**marco.silva** — 9:30 AM
"questionable dancing" is people-ops setting expectations responsibly, respect

**grace.liu** — 9:31 AM
I'm bringing a handmade bowl as a white elephant gift and I refuse to elaborate

**tom.becker** — 9:33 AM
the bowl saga has entered the holiday season

**yuki.sato** — 9:40 AM
the Amsterdam office is doing a separate borrel, we will toast to you from afar with superior beer

**priya.anand** — 9:41 AM
the EMEA flex never sleeps

---

# #data-help — 2025-12-08 — Ember Industries Enterprise critical scare

**olivia.tran** — 8:30 AM
mild panic — Ember Industries (cust_000711) showed up in the critical digest. they're a big Enterprise account ($25K MRR, 350 seats, NA-East logistics). before I escalate to elena and ruin everyone's morning — Ember critical means an uncollectible invoice, right? not usage?

**elena.volkov** — 8:35 AM
correct — **Enterprise goes critical ONLY on a recent uncollectible invoice** (`has_uncollectible_recent = true`). there's no utilization rule for Enterprise (utilization_band is NULL). so if Ember is critical, check `fact_invoices` for a recent uncollectible/failed payment.

**olivia.tran** — 8:40 AM
checked — yep, there's an invoice with `status` uncollectible from last week. so this is a billing/AR issue, not a "they hate us" issue.

**elena.volkov** — 8:42 AM
right. loop in finance/AR (rachel's team) to chase the payment. it might just be an expired card or a PO snag on their procurement side, very common with big logos. their *usage* is presumably fine?

**olivia.tran** — 8:44 AM
usage is great, they're engaged, no P1s, no detractors. purely the invoice. escalating to AR not to a save-play.

**lina.cho** — 8:50 AM
on it from finance. Ember's a good payer historically, this is almost certainly a procurement hiccup. I'll chase. and good instinct olivia — an Enterprise critical is a finance ticket, not a churn alarm.

**olivia.tran** — 8:51 AM
crisis-morning averted. ty both. the Enterprise-critical-is-billing rule has saved me from over-escalating like four times now.

---

# #data-help — 2025-12-11 — NPS segments

**newgrad.sam** — 2:00 PM
the NPS table has a `segment` column. what are the segments and how's NPS actually scored

**nina.patel** — 2:10 PM
`fact_nps_responses.score` is 0-10. standard NPS buckets: 0-6 = detractor, 7-8 = passive, 9-10 = promoter. NPS = %promoters − %detractors. the `segment` column lets you slice by customer segment (by tier or size, e.g. SMB/MM/Ent-ish) and `survey_quarter` groups the survey wave.

**newgrad.sam** — 2:12 PM
so to compute company NPS for a quarter I bucket scores into promoter/passive/detractor and do %prom − %det

**nina.patel** — 2:13 PM
exactly. and `account_health.has_recent_nps_detractor` is just "did this customer have a recent response in the 0-6 bucket." different grain — that's per-customer for the health flag, vs the aggregate NPS metric which is company- or segment-level.

**newgrad.sam** — 2:15 PM
got it. detractor = 0-6 for both, just aggregated differently. ty!

**nina.patel** — 2:16 PM
:+1: and don't mix CSAT (per-ticket) into NPS (relationship). separate tables, separate stories.

---

# #revenue — 2025-12-15 — EOY bookings, no double counting

**marcus.webb** — 9:00 AM
end of year bookings reconciliation. I want our total 2025 AE-led bookings clean for the board. @lina.cho can you pull full-year bookings_attribution and confirm we're not double-counting expansions?

**lina.cho** — 9:15 AM
```sql
SELECT SUM(bookings_acv_usd) AS total_2025_bookings,
       COUNT(*) AS n_deals
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at BETWEEN '2025-01-01' AND '2025-12-31';
```
each row is a closed-won opportunity (new OR expansion), `bookings_acv_usd` already annual. no ×12. expansions are their own opp rows (the incremental ACV), so no double-counting as long as we don't also add the base — bookings = the new/incremental annual contract value that closed.

**marcus.webb** — 9:18 AM
so an expansion shows as just the incremental ACV, not the full new contract value?

**lina.cho** — 9:20 AM
right — the `bookings_acv_usd` on an expansion opp is the *incremental* annual value (the delta), which is what you want for "new bookings." adding the customer's full new ACV would double-count the base they already had. the opp/bookings row captures the delta.

**marcus.webb** — 9:22 AM
perfect, that's clean then. total 2025 AE-led bookings = sum of bookings_acv_usd, no ×12, expansions counted as deltas. and PLG conversions are separate (not in here).

**lina.cho** — 9:23 AM
correct on all counts. PLG Free→Paid is a fact_subscriptions story, never touches bookings_attribution. your board bookings number is the AE-led annual total.

**marcus.webb** — 9:24 AM
great year. thanks lina. :rocket:

---

# #random — 2025-12-19 — holiday party recap

**marco.silva** — 9:00 AM
holiday party recap: the photo booth was a hit, the dancing was indeed questionable, and grace's white-elephant bowl was fought over with surprising intensity

**grace.liu** — 9:02 AM
MY BOWL FOUND A HOME. all the doubters can see themselves out.

**tom.becker** — 9:03 AM
I was a doubter. I am now a believer. the bowl had range.

**david.kim** — 9:05 AM
from grout to bowls, this team contains multitudes

**priya.anand** — 9:10 AM
genuinely the best #random thread arc of 2025, see you all in January, go rest :palm_tree:

---

# #data-help — 2025-12-22 — year-end ARR check before break

**rachel.stein** — 11:00 AM
before everyone scatters for the holidays — year-end ARR sanity check. `arr_snapshot` showing ~$39M, tier split Business ~$32M / Enterprise ~$6M / Pro ~$1M. that match everyone's understanding?

**lina.cho** — 11:05 AM
matches. and that's from arr_snapshot, not a dim re-sum, not a Looker tile. the $42M ghost is long dead. ~$39M is the number.

**dan.lee** — 11:08 AM
+1. and paying_customers from arr_snapshot is the canonical logo count for the year-end deck, ~520-ish paying of 800 total.

**rachel.stein** — 11:10 AM
perfect. solid year. ARR ~$39M, NRR ~1.07, GRR ~0.94. happy holidays team, see you in 2026 :christmas_tree:

**sam.reyes** — 11:15 AM
great year everyone. rest up, 2026 is going to be even bigger. :rocket: out.

---

# #random — 2026-01-05 — back from break

**sam.reyes** — 9:00 AM
happy 2026 everyone :tada: hope you all rested. big year ahead — let's make it count.

**grace.liu** — 9:05 AM
new year, new bowls

**tom.becker** — 9:06 AM
the bowl content continues into the new fiscal year, incredible

**david.kim** — 9:08 AM
my resolution is to not regrout anything for at least six months

**priya.anand** — 9:10 AM
my resolution is to finally kill the dim_customers denorm fields. (it will not happen. it never happens. but I will say it again.)

**lina.cho** — 9:11 AM
the annual tradition of priya threatening current_mrr_usd. I love it. see you at H2 planning where we don't do it again :joy:

---

# #data-help — 2026-01-08 — Linear migration chatter + a real Q

**jorge.martinez** — 10:00 AM
fyi RevOps is migrating our issue tracking from the old tool to Linear this quarter. if you have dashboards or queries that reference the old ticketing export, ping me — some of those feeds are changing. this does NOT affect `fact_support_tickets` (that's product support, different system) — just our internal RevOps/eng issue tracking.

**nina.patel** — 10:05 AM
good clarification. so `fact_support_tickets` (customer support tickets, P1/P2, CSAT) is unaffected by the Linear migration?

**jorge.martinez** — 10:06 AM
correct. `fact_support_tickets` = customer-facing support tickets, stays exactly as is. the Linear thing is our internal engineering/ops issues. totally separate. don't touch your account_health queries, the P1 signals come from fact_support_tickets and that's not moving.

**nina.patel** — 10:08 AM
phew, account_health's `has_open_p1_over_48h` reads from fact_support_tickets so I was briefly worried. all good.

**david.kim** — 10:15 AM
the number of "is this affected by the migration" questions we're going to get this quarter… jorge you should pin a "what's moving and what isn't" note

**jorge.martinez** — 10:16 AM
already drafting it. tl;dr: internal eng/ops issues → Linear. customer support tickets (fact_support_tickets) → unchanged. ARR/NRR/health marts → unchanged. it's just the internal-tooling plumbing.

**lina.cho** — 10:20 AM
+1 to pinning. and separately the Looker→ new-BI-tool eval is also happening this quarter so there's gonna be a lot of "where's my dashboard" noise. the underlying `acme` tables don't change regardless of which BI tool sits on top.

**nina.patel** — 10:22 AM
the tables are the constant, the BI tools come and go. good north star. ty both.

---

# #cs-at-risk — 2026-01-12 — Tamarind Group pause

**marco.silva** — 9:00 AM
update on Tamarind Group (cust_000706) — Business, 55 seats, NA-East insurance. they're **pausing**, not churning. their team is going through a reorg and asked to suspend for a quarter rather than cancel outright. moving them to paused status this month.

**elena.volkov** — 9:08 AM
good outcome relative to churn. so they'll be `status = 'paused'` on dim_customers. make sure whoever pulls active-logo counts knows to exclude them from "active" but NOT count them as churned.

**marco.silva** — 9:10 AM
right. and their subscription won't be is_current while paused so they'll fall out of the ARR sum automatically. it's a temporary $8,195 MRR pause, not a loss. relationship's healthy, they intend to come back.

**elena.volkov** — 9:12 AM
exactly the distinction. paused ≠ churned. for the board narrative this is a "temporary pause, reorg-driven, expected to resume" not a logo loss. tag it clearly so it doesn't get swept into churn.

**lina.cho** — 9:15 AM
noted on the finance side. paused accounts are their own bucket — ~10 of them right now across the base. Tamarind's pause drops ~$8K MRR temporarily but it's recoverable, different from the Kestrel-style budget churn.

**marco.silva** — 9:17 AM
right, Kestrel was a real loss (budget), Tamarind is a pause (reorg). keeping the buckets clean. ty.

---

# #random — 2026-01-14 — gym resolutions update

**marco.silva** — 5:00 PM
two weeks into january, status check: who's still going to the gym

**david.kim** — 5:01 PM
define "going"

**tom.becker** — 5:02 PM
I bought the shoes. the shoes are very nice. they have not left the box.

**grace.liu** — 5:03 PM
I replaced "gym" with "pottery" as my physical activity and honestly wedging clay is a workout, my forearms can attest

**olivia.tran** — 5:05 PM
grace turning pottery into cardio is the kind of optimization this company needs

**marco.silva** — 5:06 PM
the resolutions are dying on schedule, all is well

---

# #data-help — 2026-01-16 — workflow_runs_daily error columns deep dive

**newgrad.sam** — 11:00 AM
can someone explain the error columns on workflow_runs_daily? there are a bunch — auth_failed_count, rate_limited_count, step_timeout_count, integration_down_count. what's the difference and which means "our fault"?

**david.kim** — 11:12 AM
good question, here's the rundown — these map to `error_code` values on the underlying `fact_workflow_runs`:
- `AUTH_FAILED` → the customer's connected integration credentials expired/revoked (their side, usually). e.g. their Salesforce OAuth token died.
- `RATE_LIMITED` → a downstream API throttled the request. could be them hitting their own API limits, or a busy third party. usually not us.
- `STEP_TIMEOUT` → a step in the workflow took too long. could be a slow downstream API or a heavy payload.
- `INTEGRATION_DOWN` → a third-party service the workflow depends on was unavailable. their vendor, not us.

**newgrad.sam** — 11:15 AM
so none of these are really "Acme is down"?

**david.kim** — 11:17 AM
mostly no — these are the *customer-facing* failure modes, and most point at the customer's config or a third party. there are also `SCHEMA_MISMATCH` (the data shape changed unexpectedly) and `NULL_PAYLOAD` (empty input). a genuine Acme platform outage would show up differently and we'd be paging ourselves in #eng-incidents, not quietly in these counts.

**newgrad.sam** — 11:19 AM
so for CSM prep, a spike in auth_failed = "tell the customer to refresh their connection," not "apologize for an outage"

**david.kim** — 11:20 AM
exactly. that's why these columns are gold for CSMs — they tell you whose problem it is before the call. and note: there are **no step-level facts in the BI warehouse** — `step_count` is on the run, but we don't expose per-step detail in BI. if you need step-level you're going to prod, which CSMs shouldn't.

**newgrad.sam** — 11:22 AM
no step-level in BI, got it. run grain is as deep as it goes here. ty!

---

# #board-prep — 2026-01-20 — Q4 2025 board deck kickoff

**rachel.stein** — 8:00 AM
kicking off the Q4 2025 board deck. same metric sources as always, just confirming nothing's changed:
- ARR → arr_snapshot (~$39M)
- NRR/GRR → nrr_trailing_12 (~1.07 / ~0.94)
- engaged % → account_health.is_engaged (recalibrated definition, ≥3 users + ≥10 runs/28d)
all flat tables in `acme.`. confirm?

**lina.cho** — 8:10 AM
confirmed, no changes to the finance marts. arr_snapshot is the ARR source, nrr_trailing_12 is the retention source. both flat.

**rajiv.menon** — 8:15 AM
confirmed on the engagement/usage side. the recalibrated engaged definition has been the standard since Q4 2025, so this is the first *full* quarter on the new definition — no restatement footnote needed this time, it's consistently the new bar throughout Q4.

**rachel.stein** — 8:17 AM
oh nice, so Q4 is clean — entirely on the new engaged definition, no mid-quarter switch. one less footnote.

**rajiv.menon** — 8:18 AM
correct. the restatement footnote was a Q3 thing (definition changed mid-quarter). Q4 onward it's just "the definition."

**sam.reyes** — 8:30 AM
clean quarter on definitions, love it. let's build the deck. and remember the audience: lisa's going to probe retention again, have the cohort explanation ready.

**rachel.stein** — 8:31 AM
fixed-cohort, churned-stay-in-at-$0, LEFT JOIN, no inflation. I can recite it in my sleep now. on it.

---

# #random — 2026-01-23 — friday

**yuki.sato** — 4:00 PM
from Amsterdam: it is dark at 4pm and has been raining since November, please send sunlight

**grace.liu** — 4:02 PM
SF is doing that fake-summer January thing where it's 70 and sunny and everyone's confused

**yuki.sato** — 4:03 PM
I take back every coffee-superiority comment, trade you the espresso machine for some vitamin D

**marco.silva** — 4:04 PM
the EMEA office has been humbled by weather, historic day

**david.kim** — 4:05 PM
screenshotting this for the next time yuki flexes the stroopwafels

---

# #data-help — 2026-01-27 — Driftwood Media tiny account, Pro math

**grace.liu** — 10:00 AM
Driftwood Media (cust_000702) — Pro, 18 seats, NA-West media. their MRR shows as $882 and I want to sanity check that's right before I put it in a renewal summary.

**lina.cho** — 10:08 AM
$882 = 18 seats × $49/seat (Pro is $49/seat/mo). that's correct. Pro tier is $49/seat/mo, so 18 × 49 = 882. their ARR would be $882 × 12 = $10,584.

**grace.liu** — 10:10 AM
perfect, math checks. and for a Pro account utilization_band is computed (not NULL like Enterprise) right?

**lina.cho** — 10:12 AM
right — utilization_band applies to non-Enterprise (Pro/Business). for Driftwood it's active_users_28d / 18. if it's a small engaged team they could be high-utilization. only Enterprise gets the NULL utilization treatment.

**grace.liu** — 10:14 AM
Driftwood's a happy little account, good engagement for their size. renewal should be smooth. ty!

**grace.liu** — 10:15 AM
side note it's kind of nice having a tiny account after staring at the Enterprise dashboards all week, the numbers fit on one screen

**lina.cho** — 10:16 AM
the Pro accounts are a palate cleanser :joy:

---

# #cs-at-risk — 2026-01-30 — Pebble Digital low utilization

**health-bot** — 8:00 AM
:rotating_light: 2 critical. 3 at_risk. (daily 08:00 UTC digest)

**grace.liu** — 8:20 AM
one of the criticals is Pebble Digital (cust_000705) — Pro, 6 seats, EMEA martech. they're tiny ($294 MRR). a Pro going critical is utilization or uncollectible, right? checking which.

**olivia.tran** — 8:25 AM
right — non-Enterprise critical = uncollectible invoice OR utilization_band < 0.20. for a 6-seat Pro account, if only 1 user is active that's 1/6 = 0.167 → below 0.20 → critical on utilization.

**grace.liu** — 8:30 AM
checked — it's utilization. they licensed 6 seats but basically one person is using it. $294 MRR so it's not a huge dollar risk, but it's a "right-size or churn" conversation.

**olivia.tran** — 8:32 AM
yep. for a small Pro account low utilization often means they over-bought seats or the champion left and adoption stalled. worth a quick "do you want to drop to fewer seats or shall we help drive adoption" — either way better than silent churn.

**grace.liu** — 8:34 AM
on it. low-dollar but an easy save if I catch it. reaching out. ty!

**elena.volkov** — 8:40 AM
good triage. the utilization-critical Pro accounts are often the easiest saves — small, fixable, and the customer usually appreciates the proactive "are you getting value" check-in.

---

# #data-help — 2026-02-03 — Beacon Studios churn analysis

**marco.silva** — 9:00 AM
need to do the churn write-up for Beacon Studios (cust_000287) — Business, 65 seats, $9,685 MRR. they're churning Feb 18. I want to make sure the analysis correctly attributes WHY, because this one is going to come up in the QBR/board narrative.

**elena.volkov** — 9:10 AM
Beacon's an important one to get right. what's the actual driver? their health was fine, no?

**marco.silva** — 9:12 AM
that's the thing — Beacon's engagement and NPS were **healthy** right up to the churn. this is NOT product dissatisfaction. it's **procurement / parent-company driven** — their parent company is consolidating vendors after an acquisition and Beacon doesn't get to keep their own tooling decisions anymore. it's completely out of our control.

**elena.volkov** — 9:14 AM
ugh, the parent-company-consolidation churn. the worst because there's genuinely nothing to fix — the buyer was happy, the decision was made above them. make sure the churn reason is tagged as procurement/parent-company, NOT product-fit or dissatisfaction. those get conflated in the churn analysis and it skews the narrative.

**marco.silva** — 9:16 AM
exactly tagging it that way. Beacon's CSAT was good, they were engaged (well above the ≥3 users/≥10 runs bar), no detractors. the churn is 100% procurement. their champion was actually upset about losing us.

**lina.cho** — 9:20 AM
on the numbers: Beacon at $9,685 MRR ≈ $116K ARR leaving. that lands in the NRR cohort as a $0 end-MRR (LEFT JOIN keeps them in). it'll pull retention down but the *reason* tagging matters for the qualitative slide — "churn driven by external M&A/procurement, not product or satisfaction." their health metrics support that story.

**marco.silva** — 9:22 AM
right. number-wise: a ~$116K ARR churn, a zero in the cohort. story-wise: healthy account, lost to parent-company vendor consolidation, not us. both true, and the second part matters for the board.

**elena.volkov** — 9:24 AM
perfect framing. Beacon is the textbook "good churn analysis" — healthy signals + external driver = not a product problem. make sure that's crisp in the write-up.

**marco.silva** — 9:25 AM
on it. Beacon write-up: procurement/parent-company driven, healthy engagement and NPS at time of churn, ~$116K ARR, not product dissatisfaction. ty both.

---

# #random — 2026-02-05 — super bowl

**tom.becker** — 3:00 PM
super bowl squares pool in the #random channel, who's in, $10 a square

**marco.silva** — 3:01 PM
in, give me a corner square, I only win on chaos

**david.kim** — 3:02 PM
I don't watch but I'll take a square for the snacks-adjacent social credit

**grace.liu** — 3:05 PM
I'm bringing a bowl of guacamole in a handmade bowl, the bowl saga reaches the super bowl

**yuki.sato** — 3:10 PM
it'll be 1am in Amsterdam, I will not be participating, enjoy your hand-egg

**tom.becker** — 3:11 PM
"hand-egg" the EMEA office will never let us have anything

---

# #data-help — 2026-02-10 — acquisition channel breakdown

**jasmine.park** — 10:00 AM
marketing q — I want to see our customer base broken down by acquisition_channel. is that on dim_customers?

**nina.patel** — 10:08 AM
yes, `dim_customers.acquisition_channel`, one of {organic, paid_search, outbound, content, referral, partner, event, inbound}. that's how the *customer* was acquired (logo-level). note it's distinct from `bookings_attribution.first_touch_channel` which is per-deal/opportunity. for "what channel did our customers come from" use dim_customers.acquisition_channel.

**jasmine.park** — 10:10 AM
so acquisition_channel (logo-level, on the customer) vs first_touch_channel (deal-level, on bookings). when would they differ?

**nina.patel** — 10:12 AM
a customer's acquisition_channel is their original acquisition source. a single customer can have multiple opportunities over time (expansions, renewals) each with their own first_touch_channel. for a customer who came in `organic` and later had an outbound-sourced expansion, acquisition_channel = organic but the expansion opp's first_touch could be outbound. so logo-source vs deal-source.

**jasmine.park** — 10:14 AM
got it. for "where do our logos come from" → dim_customers.acquisition_channel. for "what sources our bookings" → bookings_attribution.first_touch_channel. and PLG conversions have an acquisition_channel (probably organic/content) but no bookings row.

**nina.patel** — 10:16 AM
exactly right — a Free→Paid PLG customer has an acquisition_channel on their dim row but zero presence in bookings_attribution (no opp). you're getting dangerously fluent in this data model :joy:

**jasmine.park** — 10:17 AM
this channel radicalized me. ty!

---

# #revenue — 2026-02-12 — Q1 pipeline coverage

**marcus.webb** — 9:00 AM
Q1 forecast call prep. I need pipeline coverage = open pipeline / quota target. @tom.becker can you pull open pipeline from fact_opportunities?

**tom.becker** — 9:15 AM
```sql
SELECT stage, COUNT(*) n, SUM(amount_usd) pipeline
FROM `nexus-analyst-demo.acme.fact_opportunities`
WHERE close_date BETWEEN '2026-01-01' AND '2026-03-31'
  AND stage NOT IN ('Closed Won','Closed Lost')
GROUP BY stage ORDER BY pipeline DESC;
```
that's open pipeline for Q1 by stage. coverage = that total / the Q1 quota target.

**marcus.webb** — 9:18 AM
good. and remember amount_usd on an open opp is the deal's expected ACV (annual), so no ×12 on pipeline either, same as bookings.

**tom.becker** — 9:20 AM
right — amount_usd is annual ACV, consistent with bookings_acv_usd. open pipeline and bookings are both already-annual, never ×12. coverage looks healthy for Q1, a few big Enterprise deals weighting it.

**marcus.webb** — 9:22 AM
which Enterprise deals are weighting Q1 pipeline?

**tom.becker** — 9:25 AM
the Drag Industries (cust_000412) FY26 renewal+expansion is the big one, plus a couple of net-new Ent opps. Drag's a multi-stakeholder situation, long cycle, but it's real pipeline.

**marcus.webb** — 9:27 AM
Drag is the one to watch. keep me posted on that POC/QBR motion. good coverage otherwise. thanks tom.

---

# #data-help — 2026-02-16 — Drag Industries POC metrics

**sarah.chen** — 10:00 AM
prepping the Drag Industries (cust_000412) FY26 renewal QBR. it's a big multi-stakeholder Enterprise account and I want clean usage metrics for the deck. what should I pull for an Enterprise QBR specifically?

**dan.lee** — 10:12 AM
for an Enterprise QBR, skip utilization (it's NULL for Ent) and show absolute adoption:
- active users (28d) from fact_user_events
- workflow run volume + success rate from workflow_runs_daily
- run growth trend over the contract period
- support health (P1 count, CSAT) from fact_support_tickets
- account_health_status (will be billing-driven for critical, so usually stable/healthy unless there's an AR issue)

**sarah.chen** — 10:15 AM
right, no utilization % for the Ent deck. and their health status — Drag's a healthy payer so account_health should be fine?

**dan.lee** — 10:17 AM
should be stable/healthy_expansion if they're engaged (≥3 users + ≥10 runs/28d, which a big Ent easily clears) and there's no uncollectible invoice. Enterprise only goes critical on billing, so unless AR flags something, Drag will read healthy. show the adoption trend, that's the renewal story.

**sarah.chen** — 10:20 AM
perfect. and is there a "value realization" score I can drop in to make the renewal case stronger? someone mentioned a VRS thing once.

**dan.lee** — 10:22 AM
nope — VRS is a parked draft, `vrs_band`/`champion_login_recency` don't exist. for the value story use account_health + the raw adoption metrics. those ARE your value-realization evidence, just not under a "VRS" label. account_health is the shipped reality.

**sarah.chen** — 10:24 AM
got it, no VRS, build the value story from account_health + adoption. Drag's a strong renewal, just need to show the multi-stakeholder champions the numbers. ty!

**marcus.webb** — 10:30 AM
Drag is a priority renewal. sarah keep the deck tight on adoption growth, that's what their economic buyer cares about. and loop elena's CS team for the QBR.

**sarah.chen** — 10:31 AM
will do. coordinating with olivia on the CS side.

---

# #data-help — 2026-02-18 — Greenfield SaaS discovery sizing

**yuki.sato** — 11:00 AM
discovery call with Greenfield SaaS (cust_000089) coming up. they're early-stage, exploring. I want to understand what a customer their size typically looks like in our data so I can size the opportunity. any guidance on benchmarking against similar accounts?

**nina.patel** — 11:12 AM
you can benchmark against similar-tier customers. if Greenfield's likely to land as Business (50+ seats), pull the distribution of MRR/seats/run-volume for Business accounts to set expectations:
```sql
SELECT APPROX_QUANTILES(mrr_usd, 4) AS mrr_quartiles,
       APPROX_QUANTILES(seat_count, 4) AS seat_quartiles
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current AND plan_tier = 'Business';
```
that gives you the Business-tier MRR/seat distribution to anchor the conversation.

**yuki.sato** — 11:15 AM
nice. and Business is $149/seat with a 50-seat minimum, right? so the floor is 50 × $149 = $7,450 MRR for a Business deal.

**nina.patel** — 11:17 AM
correct — Business min is 50 seats at $149/seat = $7,450/mo floor. Greenfield exploring at that tier would be ~$7,450 MRR minimum (~$89K ARR), more with extra seats. if they're smaller they might start on Pro ($49/seat, no minimum) and grow into Business.

**yuki.sato** — 11:19 AM
got it. Greenfield's a discovery/early-stage so I'll feel out whether they're a Pro-to-grow or a Business-from-the-start. ty for the benchmarking approach!

**nina.patel** — 11:20 AM
:+1: and when/if it closes-won it'll show in bookings_attribution with bookings_acv_usd (annual). good luck on the discovery.

---

# #random — 2026-02-20 — office plants

**grace.liu** — 2:00 PM
who has been overwatering the office succulents, they are not supposed to look like that

**olivia.tran** — 2:01 PM
succulents are the one plant you cannot overwater and yet we found a way

**marco.silva** — 2:03 PM
I think facilities waters them AND the cleaning crew waters them so they get double-dosed

**facilities** — 2:10 PM
we water them weekly. if they're soggy it's a rogue waterer situation, not us.

**grace.liu** — 2:11 PM
"rogue waterer" is going on a t-shirt

**david.kim** — 2:12 PM
between the rogue waterer and the cold brew bandit this office has a real unsolved-mysteries energy

---

# #data-help — 2026-02-24 — Nimbus Finance discovery, mid-market

**omar.haddad** — 10:00 AM
Nimbus Finance (cust_000601) is a mid-market discovery I'm working. they asked "how do other fintech companies use the platform." can I pull aggregate usage patterns by industry without exposing anyone's specific data?

**nina.patel** — 10:12 AM
yes, aggregate by industry. `dim_customers.industry` has the industry, join to usage:
```sql
SELECT c.industry,
       COUNT(DISTINCT c.customer_id) AS customers,
       AVG(w.success_rate) AS avg_success_rate
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.workflow_runs_daily` w USING (customer_id)
WHERE c.industry = 'fintech' AND c.status = 'active'
GROUP BY c.industry;
```
aggregate only, no individual customer exposed. that gives you "fintech customers tend to run X workflows at Y success rate."

**omar.haddad** — 10:15 AM
perfect, aggregate fintech patterns. Nimbus is mid-market (MM account_tier) so I'll frame it as "companies like you." they're in discovery so I'm just building credibility with relevant numbers.

**nina.patel** — 10:17 AM
good approach. account_tier on dim_customers is {SMB, MM, Ent} — Nimbus as MM puts them in the mid-market motion. aggregate industry benchmarks are a great discovery tool. just keep it aggregate, never name another customer's specifics.

**omar.haddad** — 10:18 AM
of course, aggregate only. ty!

**marcus.webb** — 10:25 AM
Nimbus is a good MM logo to land. omar keep me posted, mid-market deals move faster than the Enterprise slog.

**omar.haddad** — 10:26 AM
will do. ~90 day cycle for Ent but MM should be quicker, yeah.

---

# #data-help — 2026-02-26 — distinguishing new logos from expansions

**lina.cho** — 1:00 PM
PSA for anyone counting "new logos" vs "new bookings": these are different. **new logos** = net-new customers (first-ever paid subscription), countable from fact_subscriptions `change_type = 'new'` rows. **new bookings** (from bookings_attribution) includes BOTH new-logo deals AND expansion deals on existing customers. so bookings > new-logo revenue because expansions count in bookings.

**newgrad.sam** — 1:05 PM
so if I want "how many brand-new customers did we add" I count change_type = 'new' in fact_subscriptions, and if I want "total new annual contract value sold" I sum bookings_acv_usd in bookings_attribution

**lina.cho** — 1:07 PM
exactly. and `change_type` values are {new, upgrade, seat_change, churn} — there's no separate "expansion" change_type; an expansion is an `upgrade` or a `seat_change` row where mrr_usd went up (follow `changed_from_subscription_id` to see the prior state). a downgrade is a seat_change where mrr went down.

**newgrad.sam** — 1:09 PM
no "downgrade" change_type, it's a seat_change with lower mrr. and no "expansion" change_type either, it's upgrade/seat_change with higher mrr. got it.

**lina.cho** — 1:10 PM
right. the change_type tells you the *kind* of event; the mrr delta (vs the changed_from row) tells you the direction. and a Free→Paid PLG conversion is a `new` (or upgrade from Free) row, not a bookings row.

**newgrad.sam** — 1:12 PM
this is the change_type masterclass I didn't know I needed. saving it. ty!

**dan.lee** — 1:15 PM
bookmarking this thread, it answers like five recurring questions at once. lina you should turn it into a glossary entry.

**lina.cho** — 1:16 PM
adding it to `glossary__churn_rate.md` and maybe a new logos/bookings gloss. good idea.

---

# #random — 2026-02-27 — friday

**david.kim** — 4:30 PM
it has been six weeks and I have not regrouted anything, resolution intact

**grace.liu** — 4:31 PM
meanwhile I've made four more bowls, my apartment is becoming a bowl museum

**tom.becker** — 4:32 PM
the shoes have left the box. I went for one (1) run. the resolution lives, barely.

**olivia.tran** — 4:33 PM
tom's one run is the most inspiring fitness content of Q1

**yuki.sato** — 4:40 PM
from Amsterdam: the sun came out for 20 minutes today and the entire city went outside, it was beautiful and now it's raining again

**marco.silva** — 4:41 PM
20 minutes of EMEA sunlight, treasure it

---

# #data-help — 2026-03-02 — Willow Works LATAM, Pro renewal

**grace.liu** — 9:30 AM
Willow Works (cust_000709) renewal — Pro, 25 seats, LATAM gaming. MRR $1,225. sanity check the math and I want their engagement status.

**lina.cho** — 9:40 AM
$1,225 = 25 × $49 (Pro). correct. for engagement check account_health.is_engaged — needs ≥3 active users AND ≥10 successful runs / trailing 28d.

**grace.liu** — 9:42 AM
they're engaged, good usage for a gaming studio. utilization is decent too (it's a Pro so utilization_band is computed). smooth renewal expected.

**lina.cho** — 9:44 AM
nice. 25 × $49 = $1,225 MRR, ~$14.7K ARR. small but healthy. LATAM region, organic acquisition if I recall. good little account.

**grace.liu** — 9:45 AM
yep organic. easy renewal. ty for the math check!

---

# #data-help — 2026-03-04 — Sable Analytics expansion modeling

**sarah.chen** — 10:00 AM
Sable Analytics (cust_000710) wants to add seats. they're Business, currently 90 seats / $13,410 MRR, EMEA fintech. if they go to 130 seats what's the new MRR and how does it book?

**lina.cho** — 10:10 AM
130 × $149 (Business) = $19,370 MRR. they're at 90 × $149 = $13,410 now. so the expansion is +40 seats = +$5,960 MRR = +$71,520 incremental ACV. when it closes-won, bookings_attribution gets a row with bookings_acv_usd = the incremental ~$71,520 (annual, no ×12), not the full new contract value.

**sarah.chen** — 10:13 AM
so the booking is just the delta (40 seats worth), not the whole 130-seat contract value.

**lina.cho** — 10:15 AM
right — bookings = incremental annual value. the base $13,410 they already had isn't re-booked. only the +$5,960/mo × 12 = ~$71,520 new ACV counts as the expansion booking. and it shows as a seat_change/upgrade row in fact_subscriptions with the higher mrr_usd.

**sarah.chen** — 10:17 AM
clean. 90→130 seats, +$5,960 MRR, ~$71.5K incremental ACV booking. Sable resolved their integration gripe from a while back and now they're expanding, nice turnaround.

**lina.cho** — 10:18 AM
love a detractor-to-expansion arc. that's the CS/sales motion working. partner-sourced too. ty for keeping the ACV math clean (no ×12 on that delta).

**sarah.chen** — 10:19 AM
the ×12 trauma is permanent at this point :sweat_smile:

---

# #cs-at-risk — 2026-03-06 — Harbor Dynamics P1 escalation

**health-bot** — 8:00 AM
:rotating_light: 1 critical. 4 at_risk. (daily 08:00 UTC digest)

**marco.silva** — 8:20 AM
Harbor Dynamics (cust_000713) is one of the at_risk — Business, 150 seats, APAC insurance, $22,350 MRR. that's a meaningful account. checking if it's P1 or NPS.

**olivia.tran** — 8:25 AM
pull the flags:
```sql
SELECT has_open_p1_over_48h, n_open_p1_over_48h, has_recent_nps_detractor
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000713';
```

**marco.silva** — 8:30 AM
it's `has_open_p1_over_48h = true`, n_open_p1_over_48h = 1. so they have one P1 support ticket open more than 48 hours. that's what tripped at_risk. not an NPS thing.

**olivia.tran** — 8:32 AM
ok so this is a support-escalation, not a relationship problem. find the ticket and whoever owns it:
```sql
SELECT ticket_id, opened_at, priority, category, assigned_to_employee_id
FROM `nexus-analyst-demo.acme.fact_support_tickets`
WHERE customer_id = 'cust_000713' AND priority = 'P1' AND closed_at IS NULL
ORDER BY opened_at;
```
then go light a fire under that ticket. a P1 sitting >48h on a $22K MRR account is exactly what at_risk is built to surface.

**marco.silva** — 8:35 AM
got it, found the open P1, escalating to support leadership now. Harbor's a good account otherwise, engaged, no detractors — just this one stuck ticket. once it closes the at_risk should clear next refresh.

**elena.volkov** — 8:40 AM
exactly the right use of the signal. P1>48h = drop everything. and remember only P1 trips this — a P2 sitting for days wouldn't show here, which is a separate gap we live with. close that P1.

**marco.silva** — 8:41 AM
on it. P1 only, P2 doesn't escalate, noted again. fixing.

---

# #random — 2026-03-07 — daylight savings again

**priya.anand** — 8:00 AM
daylight savings this weekend (US). the standup poll wounds reopen. the 9:45 slot becomes a lie once more.

**david.kim** — 8:01 AM
I have made peace with the eternal time war. wake me when we adopt permanent DST.

**yuki.sato** — 8:05 AM
EMEA switches in two weeks so for a fortnight the cross-office calls will be off by an hour and chaos will reign

**nina.patel** — 8:06 AM
the "is this meeting at the time I think it is" anxiety for the next two weeks is going to be something

**jorge.martinez** — 8:10 AM
I will send a calendar PSA, as is tradition, that nobody will read, as is tradition

---

# #data-help — 2026-03-10 — Quartz Foundry Enterprise health

**olivia.tran** — 10:00 AM
Quartz Foundry (cust_000714) check-in — Enterprise, 280 seats, EMEA healthtech, $12K MRR, partner-sourced. they closed-won back in Q3 and I'm doing the post-onboarding health review. what does a healthy Enterprise onboarding look like in the data?

**dan.lee** — 10:12 AM
for a healthy Enterprise onboarding you want to see, over the first ~90 days:
- active users ramping (more of their licensed team logging in over time)
- workflow run volume climbing (they're building real automations)
- success rate stabilizing high (>95%-ish once they've debugged their integrations)
- no uncollectible invoices (the only thing that'd make an Ent critical)
- is_engaged = true (≥3 users + ≥10 runs/28d, which they should clear easily at 280 seats)

**olivia.tran** — 10:15 AM
Quartz is ramping nicely — users climbing, runs climbing, success rate ~96%, engaged, clean invoices. healthy onboarding. account_health_status should be stable or healthy_expansion.

**dan.lee** — 10:17 AM
if they're engaged AND utiliz— wait, no, Quartz is Enterprise so utilization_band is NULL, healthy_expansion's utilization≥0.6 clause doesn't apply the same way. for Enterprise, healthy_expansion is driven by engagement + the absence of risk flags. they'll read healthy. the utilization≥0.6 part of healthy_expansion is really a non-Enterprise thing.

**olivia.tran** — 10:19 AM
right, Enterprise doesn't have utilization so healthy_expansion for them leans on engagement + no risk flags. Quartz qualifies. great onboarding, partner-sourced account paying off. ty!

**elena.volkov** — 10:25 AM
Quartz is a poster-child onboarding. good for the partner-channel QBR story — partner-sourced Enterprise that onboarded clean and is expanding. lean into it.

---

# #board-prep — 2026-03-12 — Q4/FY25 retention deep dive

**rachel.stein** — 8:30 AM
board wants a retention deep-dive for the FY25 wrap. I want to show NRR and GRR with the churn breakdown by reason. @lina.cho can we decompose the GRR drag into churn buckets?

**lina.cho** — 8:45 AM
yes. GRR ~0.94 means ~6 points of gross revenue lost over the cohort. decomposing the churn buckets qualitatively:
- procurement/M&A-driven (e.g. Beacon Studios — healthy account lost to parent-company vendor consolidation, ~$116K ARR)
- budget cuts (e.g. Kestrel Networks — fine usage, lost their own funding, ~$125K ARR)
- product-fit (the smaller cohort — e.g. some Pro/SMB accounts that outgrew or under-adopted)
- downgrades to Free (counted as churn for revenue even though logo survives)

the *numbers* all land the same way in the cohort (LEFT JOIN, $0 end MRR). the *reasons* are the narrative.

**rachel.stein** — 8:48 AM
that's exactly the slide — GRR 0.94, and here's WHY the 6 points left, mostly external (procurement/budget) not product. the Beacon and Kestrel examples make it concrete and both were healthy-at-churn.

**lina.cho** — 8:50 AM
right. the encouraging board message: most of our gross churn is external/uncontrollable (M&A, budget) on otherwise-healthy accounts, not customers fleeing a bad product. NRR ~1.07 means expansion more than covers it. the reason-tagging is what lets us tell that story credibly.

**sam.reyes** — 9:00 AM
this is the narrative I want. "we lose some logos to forces outside our control, but the customers who stay expand, net 1.07." and we can back every churn with a reason. strong story. build it.

**rachel.stein** — 9:01 AM
on it. retention deep-dive: NRR 1.07, GRR 0.94, churn-by-reason mostly external, expansion covers the gap. :muscle:

**elena.volkov** — 9:05 AM
+1, and CS can speak to each named churn if the board probes. Beacon = procurement, Kestrel = budget, both healthy. we have the receipts.

---

# #random — 2026-03-14 — pi day

**david.kim** — 11:00 AM
it's pi day (3.14), someone brought actual pie to the 2nd floor kitchen, this is the engineering holiday we deserve

**nina.patel** — 11:02 AM
pie-driven development is the only methodology I trust

**grace.liu** — 11:03 AM
I'd put a slice in one of my bowls but the bowls are not, structurally, to be trusted with liquid pie filling

**marco.silva** — 11:05 AM
"not to be trusted with liquid" is the most honest pottery review ever given

**yuki.sato** — 11:10 AM
in Europe pi day would be 14.3 which isn't pi, so we don't get pie, the injustice compounds

**tom.becker** — 11:11 AM
the EMEA office robbed of both football respect AND pi day pie, tragic

---

# #data-help — 2026-03-18 — Verdant Cloud recovery

**olivia.tran** — 10:00 AM
good news follow-up — Verdant Cloud (cust_000707), the Enterprise account that dropped to monitoring back in October when their runs cratered? they're back. we helped them fix the broken workflow, successful runs recovered, they're engaged again.

**dan.lee** — 10:08 AM
nice! so they crossed back over the engaged bar (≥3 users + ≥10 successful runs/28d)?

**olivia.tran** — 10:10 AM
yep. their active users never dropped, it was always the successful-runs side — one critical workflow was failing and dragging successful runs under 10/28d. once support helped them fix the broken integration, runs recovered, is_engaged flipped back to true, status back to stable.

**dan.lee** — 10:12 AM
that's the engagement signal doing its job — caught the dip early (a workflow broke), CS intervened, recovered before renewal. textbook proactive save. and it shows why "successful" runs matter, not just runs — a failing workflow still "runs" but doesn't count toward engagement.

**olivia.tran** — 10:14 AM
exactly — n_success vs n_runs. a customer can have tons of runs but if they're failing, successful runs (the engagement input) stays low. Verdant's runs were happening, just failing. fixed now. great outcome for an APAC ecommerce account. ty!

**elena.volkov** — 10:20 AM
Verdant's a great proactive-CS case study. the monitoring flag → outreach → fix → re-engaged loop is exactly the playbook. nice work olivia.

---

# #data-help — 2026-03-20 — marketing touches multi-touch

**jasmine.park** — 10:00 AM
I want a multi-touch view of how customers engage with marketing before they convert. `fact_marketing_touches` has every touch right? how do I trace a customer's journey?

**nina.patel** — 10:12 AM
yep, `fact_marketing_touches` is the granular per-touch table. columns: `touch_id`, `lead_email_hash` (PII-hashed), `customer_id` (populated once they're a known customer), `touched_at`, `channel`, `campaign`, `utm_source/medium/campaign`, `attributed_revenue_usd`. to trace a journey, order by touched_at for a customer_id.

**jasmine.park** — 10:14 AM
so the FIRST row by touched_at is the first-touch (which matches bookings_attribution.first_touch_channel for deals)?

**nina.patel** — 10:16 AM
right — bookings_attribution.first_touch_channel is essentially the channel of the earliest attributed touch in fact_marketing_touches for that customer's journey. fact_marketing_touches is the full path; bookings_attribution just carries the first-touch summary for closed-won deals. attributed_revenue_usd is the modeled attribution credit per touch.

**jasmine.park** — 10:18 AM
and for leads who never became customers, customer_id is null but lead_email_hash links their touches?

**nina.patel** — 10:20 AM
exactly. pre-conversion, touches are keyed by lead_email_hash. once they convert and we resolve identity, customer_id gets populated. so you can do full-funnel from anonymous lead → known customer. just remember attributed_revenue is a *model*, not actuals — for actual bookings use bookings_attribution (no ×12, annual).

**jasmine.park** — 10:22 AM
got it. fact_marketing_touches = full journey + modeled attribution, bookings_attribution = actual closed-won annual ACV by first-touch. ty!

---

# #data-help — 2026-03-23 — engaged % trend question

**dan.lee** — 11:00 AM
PM asked for the engaged-% trend over the last year and I want to flag the definition-change caveat clearly. anyone pulling this: the **engaged definition was recalibrated in Q4 2025** (tightened to ≥3 active users AND ≥10 successful runs/28d from a looser prior bar). if you pull a raw trailing series, the pre-Q4 points are on the OLD definition and will look artificially higher.

**newgrad.sam** — 11:05 AM
so how do I show a clean trend?

**dan.lee** — 11:07 AM
two options: (1) restate the whole series on the new definition (rajiv did this for the board deck — re-run the ≥3/≥10 logic across all historical 28d windows), or (2) show the series but footnote the Q4 2025 break and don't let anyone read the pre/post jump as real movement. option 1 is cleaner if you have the compute.

**rajiv.menon** — 11:12 AM
I have the restated series cached from the board work — the new definition applied consistently across all periods. ping me and I'll point you at it. do NOT mix old-definition historical points with new-definition recent points, that's a fake trend.

**newgrad.sam** — 11:14 AM
using the restated series. ≥3 active users AND ≥10 successful runs / trailing 28d, applied consistently. got it. ty!

**dan.lee** — 11:15 AM
this is the kind of thing that generates a "why did engagement drop in Q4" question when really we just moved the goalposts. restate or footnote, always.

---

# #random — 2026-03-25 — spring

**grace.liu** — 2:00 PM
spring has sprung, the office succulents survived the rogue waterer, and I have started a new pottery series (mugs this time, ambitious)

**olivia.tran** — 2:01 PM
from bowls to mugs, grace is diversifying the ceramic portfolio

**david.kim** — 2:03 PM
mugs have handles, that's a whole new structural challenge, godspeed

**grace.liu** — 2:04 PM
the first three mugs have handles that are "decorative" (do not hold weight)

**marco.silva** — 2:05 PM
"decorative handles" the bowl-to-mug pipeline has the same liquid-trust issues as before

**grace.liu** — 2:06 PM
my pottery's defining feature remains: do not put anything in it

---

# #data-help — 2026-03-27 — Cobalt Systems expansion check

**tom.becker** — 10:00 AM
Cobalt Systems (cust_000700) is talking expansion. Business, currently 80 seats / $11,920 MRR, EMEA fintech, outbound-sourced. their auth_failed issues from last summer — are those resolved? want to make sure usage is healthy before I pitch more seats.

**david.kim** — 10:10 AM
let me pull their recent workflow_runs_daily. their AUTH_FAILED spike was August (expired integration token on their side). checking current:

**david.kim** — 10:13 AM
they're clean now — auth_failed_count back to baseline, success rate ~96%, run volume up. the token issue resolved once their admin re-authed. healthy usage, good expansion candidate.

**tom.becker** — 10:15 AM
perfect. so if they add say 40 seats → 120 × $149 = $17,880 MRR, expansion of +$5,960/mo = ~$71.5K incremental ACV booking (annual, no ×12).

**david.kim** — 10:17 AM
math checks (80→120 = +40 × $149 = +$5,960 MRR). and their health supports it — engaged, clean runs, no risk flags. account_health should read stable/healthy_expansion. go pitch it.

**tom.becker** — 10:18 AM
Cobalt's been a solid account since they fixed the auth thing. expanding. ty for the health check!

**marco.silva** — 10:25 AM
+1 from CS, Cobalt's champion is happy, the auth thing was their IT not us, and they know it. good expansion. tom go get it.

---

# #cs-at-risk — 2026-03-30 — month-end health digest

**health-bot** — 8:00 AM
:rotating_light: 2 critical. 3 at_risk. 1 newly monitoring. (daily 08:00 UTC digest — month-end)

**elena.volkov** — 8:15 AM
month-end digest. let's clear the board before the new month. marco/olivia/grace — divide and conquer. and a reminder on the rules since we onboarded two new CSMs this month:
- **critical**: Enterprise = uncollectible invoice ONLY. Non-Enterprise = uncollectible OR utilization_band < 0.20.
- **at_risk**: open P1 >48h OR recent NPS detractor.
- **healthy_expansion**: engaged AND (for non-Ent) utilization ≥ 0.6.
- **monitoring**: not engaged (the lukewarm bucket).
- engaged = ≥3 active users AND ≥10 successful runs / trailing 28d.

**marco.silva** — 8:20 AM
taking the two criticals. one's an Ent (so: billing — checking invoices) and one's a non-Ent (so: billing or utilization — checking both).

**olivia.tran** — 8:22 AM
I've got two of the at_risk — checking P1 vs NPS on each.

**grace.liu** — 8:23 AM
I'll take the third at_risk + the new monitoring one. monitoring = engagement dipped, so I'll check whose runs or users dropped.

**elena.volkov** — 8:25 AM
perfect. all signals come from `acme.account_health` (flat table — not a nested path, not VRS). pull the row, read the flags, work the playbook. report back by EOD.

**marco.silva** — 9:30 AM
update: my Ent critical is an expired-card uncollectible (finance chasing), my non-Ent critical is utilization (a Pro that over-bought seats — right-sizing convo). neither is a product/churn emergency.

**olivia.tran** — 9:35 AM
my two at_risk: one P1>48h (escalated to support), one NPS detractor (reaching out, it's a feature gripe). both actionable.

**grace.liu** — 9:40 AM
my at_risk is a P1, escalated. the monitoring one had a champion go on leave so their active users dipped under 3 — temporary, reaching out to find a backup admin.

**elena.volkov** — 9:42 AM
beautiful triage everyone. that's the board cleared and every flag understood. this is exactly how account_health is supposed to drive the day. nice work.

---

# #random — 2026-03-31 — Q1 close vibes

**sam.reyes** — 5:00 PM
Q1 2026 in the books :tada: strong quarter. thank you all. the metrics tell a great story and you're the ones who built it (and who keep this #data-help channel from descending into pure chaos, mostly).

**lina.cho** — 5:02 PM
the channel is 60% data questions, 40% grout and bowls, and honestly that ratio is sacred

**grace.liu** — 5:03 PM
I'll have a commemorative Q1 mug ready by next week (handle: decorative)

**david.kim** — 5:04 PM
the mug will not hold coffee but it will hold meaning

**marco.silva** — 5:05 PM
great quarter team. the criticals were mostly billing and external, the expansions were real, NRR's holding. couldn't ask for more. :rocket:

**rachel.stein** — 5:06 PM
ARR ~$39M, NRR ~1.07, GRR ~0.94, clean definitions, no $42M ghosts. a finance person's dream quarter. well done all. :champagne:

---

# #data-help — 2025-07-23 — invoice status values

**newgrad.sam** — 1:00 PM
what are the possible `status` values on fact_invoices? I'm trying to find unpaid/problem invoices for a finance ask.

**lina.cho** — 1:10 PM
`fact_invoices.status` is roughly {paid, open, void, uncollectible}. `paid` = collected (has a `paid_at`), `open` = issued not yet paid (within terms), `void` = cancelled, `uncollectible` = written off / failed collection. for "problem" invoices you usually want `uncollectible` (and `open` past due_date if you want at-risk-of-becoming-uncollectible).

**newgrad.sam** — 1:12 PM
and `has_uncollectible_recent` on account_health reads from the uncollectible ones?

**lina.cho** — 1:14 PM
exactly — `has_uncollectible_recent = true` means the customer has a recent uncollectible invoice. that's the signal that makes an **Enterprise account critical** (it's the ONLY Enterprise-critical rule), and it's one of the two non-Enterprise critical triggers (the other being utilization<0.20).

**newgrad.sam** — 1:16 PM
so a recent uncollectible = critical regardless of tier, just for different "only" reasons. got it. ty!

**lina.cho** — 1:17 PM
right. uncollectible is bad news at any tier. for Enterprise it's the sole critical trigger; for others it's one of two. fact_invoices.status = 'uncollectible' is the source.

---

# #data-help — 2025-08-01 — region values and slicing

**jasmine.park** — 10:00 AM
what are the region values? I want to slice the customer base geographically for a campaign.

**nina.patel** — 10:08 AM
`dim_customers.region` is one of {NA-East, NA-West, EMEA, APAC, LATAM}. and there's a separate `country` field for finer geography. region is the coarse bucket we use for territory/reporting.

**jasmine.park** — 10:10 AM
so NA is split East/West but EMEA/APAC/LATAM are single buckets

**nina.patel** — 10:11 AM
right, NA gets the East/West split (sales territory reasons), the rest are single regions. our HQ is SF (NA-West) and the EMEA office is Amsterdam, which is why those two regions have the most accounts. if you want country-level use the `country` field.

**jasmine.park** — 10:13 AM
perfect. region for the coarse cut, country if I need to drill. ty!

**yuki.sato** — 10:20 AM
EMEA represent :netherlands: (from the superior-espresso office)

**nina.patel** — 10:21 AM
the region thread became an EMEA flex within 13 minutes, a new record

---

# #random — 2025-08-14 — fantasy football draft

**tom.becker** — 4:00 PM
fantasy football draft is next week, the #random league is reforming, $20 buy-in, loser buys lunch for the office

**marco.silva** — 4:01 PM
in. I will draft chaotically and lose with dignity

**david.kim** — 4:02 PM
I'll join purely to deny tom a victory

**yuki.sato** — 4:05 PM
American football fantasy at 1am Amsterdam time, I'll auto-draft and accept my fate

**tom.becker** — 4:06 PM
yuki auto-drafting and somehow winning would be the funniest possible outcome

**grace.liu** — 4:10 PM
I'm out, I'll be at pottery, but I'll make the trophy (a bowl, obviously)

**tom.becker** — 4:11 PM
THE LEAGUE TROPHY IS A GRACE BOWL, this is now the most prestigious league in existence

---

# #data-help — 2025-08-28 — dim_employees for CSM/AE lookups

**marco.silva** — 11:00 AM
how do I map a customer to their CSM and AE names? I have csm_employee_id and ae_employee_id on dim_customers but I want the actual names for a report.

**nina.patel** — 11:10 AM
join to `dim_employees` on employee_id:
```sql
SELECT c.customer_id, c.company_name,
       csm.full_name AS csm_name, ae.full_name AS ae_name
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` csm ON c.csm_employee_id = csm.employee_id
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` ae  ON c.ae_employee_id  = ae.employee_id
WHERE c.status = 'active';
```
dim_employees has full_name, team, role, manager_employee_id, hire_date, termination_date, location, is_active.

**marco.silva** — 11:13 AM
perfect. and if an employee left (terminated), their accounts would still reference the old employee_id?

**nina.patel** — 11:15 AM
yes — historical references stay. dim_employees.is_active / termination_date tells you who's current. if you only want active reps filter `csm.is_active = true`. for accounts whose CSM left and hasn't been reassigned you'd see a terminated employee on the FK until reassignment.

**marco.silva** — 11:17 AM
got it. LEFT JOIN so I don't drop customers with an unreassigned rep, then filter is_active if I want current only. ty!

**elena.volkov** — 11:25 AM
useful — also if you're auditing CSM book-of-business balance, that join is how you count accounts per CSM. marco/olivia/grace each carry a chunk of the ~745 active accounts.

---

# #data-help — 2025-09-04 — billing_cycle and annual vs monthly

**lina.cho** — 9:00 AM
clarifying a recurring confusion: `fact_subscriptions.billing_cycle` tells you how the customer is *billed* (monthly vs annual), but `mrr_usd` is ALWAYS a monthly-normalized figure regardless. so an Enterprise customer billed annually still has `mrr_usd = annual_contract_value / 12`. don't try to "un-annualize" mrr_usd based on billing_cycle — it's already monthly.

**newgrad.sam** — 9:05 AM
so billing_cycle is about invoicing rhythm, mrr_usd is always monthly-normalized

**lina.cho** — 9:07 AM
exactly. billing_cycle = annual means they get one big invoice a year (you'll see it in fact_invoices), but for MRR/ARR math mrr_usd is monthly and ARR = mrr_usd × 12. the billing_cycle doesn't change the MRR normalization. this trips people up: "they pay annually so isn't their MRR the whole amount?" — no, mrr_usd is normalized monthly.

**newgrad.sam** — 9:09 AM
ok so the ×12 to ARR works uniformly because mrr_usd is uniformly monthly, regardless of how they're invoiced

**lina.cho** — 9:10 AM
you got it. uniform monthly mrr_usd → uniform ×12 → ARR. billing_cycle is just invoicing cadence (matters for cash-flow/AR timing, not for MRR/ARR). and arr_snapshot bakes all this so the board number is consistent.

**newgrad.sam** — 9:11 AM
the ×12 lore deepens. ty!

---

# #random — 2025-09-18 — coffee machine update (resolved-ish)

**marco.silva** — 10:00 AM
the SF coffee machine has been descaled, runs quietly, and produces actual coffee. a golden age has begun.

**facilities** — 10:05 AM
we also put a laminated "how to run the cleaning cycle" card on it. please use it BEFORE it reaches dying-robot status next time.

**marco.silva** — 10:06 AM
laminated. they laminated it. facilities is not playing.

**olivia.tran** — 10:07 AM
the lamination is a power move and I respect it completely

**yuki.sato** — 10:15 AM
the Amsterdam machine has never once needed an intervention, just saying, for the record, again

**marco.silva** — 10:16 AM
WE GET IT YUKI. enjoy your perfect espresso and your 4pm darkness.

---

# #data-help — 2025-10-02 — current_plan_tier vs subscription tier

**aliyah.brooks** — 1:00 PM
quick one — `dim_customers.current_plan_tier` vs the `plan_tier` on the current fact_subscriptions row. should those always agree?

**lina.cho** — 1:10 PM
in steady state yes, but dim is a nightly denorm so it can lag the fact by up to ~24h. if a customer changed plans today, the fact_subscriptions `is_current` row reflects it immediately but dim's `current_plan_tier` won't update until the nightly job runs. so they can disagree for <24h. fact is authoritative.

**aliyah.brooks** — 1:12 PM
so same lesson as current_mrr_usd — dim is a lagging convenience denorm, fact is truth

**lina.cho** — 1:13 PM
exactly. both `current_plan_tier` and `current_mrr_usd` on dim are nightly denorms for ad-hoc filtering. for anything board-grade or count-sensitive, go to fact_subscriptions (is_current). the off-by-a-few count discrepancies people hit are almost always this lag.

**aliyah.brooks** — 1:15 PM
our marketing dashboard uses current_plan_tier for filter chips, which you've told me before is fine for filtering

**lina.cho** — 1:16 PM
totally fine for filter chips / personalization. the only "wrong" is if you report a board number off the dim. filtering "show me Pro customers" tolerates a <24h lag on a handful of accounts. ty for double-checking though, better safe.

**aliyah.brooks** — 1:17 PM
the dim-vs-fact gospel is fully internalized now. ty!

---

# #data-help — 2025-10-16 — renewal_forecast table existence

**grace.liu** — 2:00 PM
the dbt repo references `models/marts/cs/renewal_forecast.sql` — is there an `acme.renewal_forecast` table I can query for renewal dates/risk?

**dan.lee** — 2:10 PM
careful here — that's a dbt model *path*, downstream of account_health, but I'm not certain it's actually materialized to BigQuery. before you query `acme.renewal_forecast`, verify it exists:
```sql
SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES`
WHERE table_name = 'renewal_forecast';
```
if it comes back empty, it's a model that's defined in dbt but not built (or built elsewhere). don't assume the folder path = a live table.

**grace.liu** — 2:14 PM
ran it — comes back empty. so renewal_forecast isn't a materialized table right now?

**dan.lee** — 2:16 PM
right, not currently materialized in `acme`. the .sql exists in the repo but it's either disabled, ephemeral, or WIP. for renewal-relevant data today, build off `acme.account_health` (the risk signals) + `fact_subscriptions` (end_date / contract dates) + `fact_opportunities` (renewal opps). don't query a table that isn't there.

**grace.liu** — 2:18 PM
got it — same lesson as the VRS thing basically. a dbt model existing in the repo doesn't mean there's a queryable table. verify with INFORMATION_SCHEMA. using account_health + fact_subscriptions for renewals.

**dan.lee** — 2:20 PM
exactly. the repo has more model files than we have materialized tables — some are parked, disabled, or WIP (renewal_forecast, the VRS draft, etc). `INFORMATION_SCHEMA.TABLES` is the ground truth for "does this table exist." the ~13 real tables (5 dims, 8 facts) + the materialized marts are what's actually queryable.

**grace.liu** — 2:22 PM
INFORMATION_SCHEMA as the existence oracle. adding to the sticky-note collection. ty!

**rajiv.menon** — 2:30 PM
+1 to dan. as the dbt owner: not every model in the repo is materialized to `acme`. some are `enabled: false`, some are dev-only. always verify against INFORMATION_SCHEMA before building a query on a table you've only seen in the dbt folder structure. and remember it's flat — `acme.renewal_forecast`, never `acme.marts.cs.renewal_forecast`, IF it existed (it doesn't right now).

---

# #data-help — 2025-10-23 — churn rate formula

**newgrad.sam** — 10:00 AM
how do we calculate churn rate? logo churn specifically. is it just churned / total?

**lina.cho** — 10:10 AM
logo churn rate over a period = (logos that churned during the period) / (logos at the start of the period). so it's churned-in-period over starting-count, not churned over current-total. pick your period (monthly, quarterly, annual) and be consistent. for revenue churn it's churned MRR / starting MRR.

**newgrad.sam** — 10:12 AM
so denominator is START-of-period count, not end or current

**lina.cho** — 10:14 AM
right, start-of-period. if you start a quarter with 500 paying logos and 10 churn during it, that's 10/500 = 2% quarterly logo churn. and remember the Free-downgrade nuance: a downgrade to Free is *revenue* churn (counts in revenue churn rate) but the logo technically survives (might not count in *logo* churn depending on your definition). be explicit which churn you mean.

**newgrad.sam** — 10:16 AM
logo churn (they left entirely) vs revenue churn (they stopped paying, incl Free downgrade). different denominators-of-pain. got it.

**lina.cho** — 10:17 AM
"denominators of pain" lol. yes. and this connects to NRR/GRR: GRR ~0.94 means ~6% gross revenue churn over the trailing year on the cohort. logo churn and revenue churn rarely match exactly because of downgrades and because big-vs-small logos churn at different rates.

**newgrad.sam** — 10:19 AM
the metrics all interconnect and it's beautiful and slightly terrifying. ty!

---

# #random — 2025-10-31 — halloween

**grace.liu** — 11:00 AM
happy halloween, my costume is "ceramicist who has given up on functional pottery" which is just me holding a bowl

**marco.silva** — 11:02 AM
that's not a costume that's a documentary

**david.kim** — 11:03 AM
I'm going as "the rogue waterer," it's a subtle costume, only facilities will understand it

**facilities** — 11:10 AM
we understand it. we're watching you.

**david.kim** — 11:11 AM
the facilities team having a sense of humor is the real halloween treat

**yuki.sato** — 11:20 AM
halloween is bigger in the US, in NL it's more of a soft thing, but I carved a pumpkin out of solidarity and it's already moldy because of the rain

**marco.silva** — 11:21 AM
even yuki's pumpkin is defeated by Amsterdam weather, the saga continues

---

# #data-help — 2025-11-06 — seat utilization edge cases

**grace.liu** — 1:00 PM
edge case on utilization_band — what happens if a customer has more active users than licensed seats? can utilization go above 1.0?

**dan.lee** — 1:10 PM
good edge case. it can happen if, say, they have 10 licensed seats but 12 distinct users logged in during the 28d window (over-provisioning, shared logins, or a seat-count that's behind the actual usage). utilization_band would be 1.2 in that case. it's not capped at 1.0 — it's a raw ratio. but it's a flag that they probably need MORE seats (expansion opportunity!) or that there's a seat-compliance question.

**grace.liu** — 1:12 PM
so utilization > 1.0 = they're using more than they pay for = either expand them or a compliance nudge

**dan.lee** — 1:14 PM
right. and `healthy_expansion` status keys partly off utilization ≥ 0.6, so a >1.0 utilization (non-Ent) is a strong expansion signal — they're clearly getting value and bumping the seat ceiling. for Enterprise this whole thing is moot (utilization_band NULL, unlimited seats). over-utilization on a Pro/Business is a sales tap-on-the-shoulder.

**grace.liu** — 1:16 PM
love that — an over-utilization flag is a happy problem, an expansion lead. and under 0.20 is the critical/right-size problem. utilization tells two stories at the extremes.

**dan.lee** — 1:18 PM
exactly. <0.20 = critical (they're not using what they pay for), ≥0.6 = healthy_expansion candidate, >1.0 = definitely expand them. the band is one of the most actionable columns for non-Enterprise CS/sales.

**grace.liu** — 1:19 PM
utilization_band: the column with range. (unlike my mugs.) ty!

---

# #data-help — 2025-11-12 — cohort retention SQL pattern

**nina.patel** — 10:00 AM
someone asked me for a generic monthly cohort-retention query (not the board NRR, just a "do customers signed up in month X stick around" view). dropping a pattern here since it comes up:
```sql
WITH cohorts AS (
  SELECT customer_id, DATE_TRUNC(signup_date, MONTH) AS cohort_month
  FROM `nexus-analyst-demo.acme.dim_customers`
),
activity AS (
  SELECT DISTINCT customer_id, DATE_TRUNC(DATE(event_at), MONTH) AS active_month
  FROM `nexus-analyst-demo.acme.fact_user_events`
)
SELECT c.cohort_month, a.active_month,
       COUNT(DISTINCT c.customer_id) AS retained
FROM cohorts c JOIN activity a USING (customer_id)
GROUP BY 1,2 ORDER BY 1,2;
```
that's activity-based cohort retention. note this is DIFFERENT from the board NRR (which is revenue-based, fixed-cohort, trailing-12).

**newgrad.sam** — 10:08 AM
so this is "are they still active" cohort retention, vs NRR which is "are they still paying (and how much)"

**nina.patel** — 10:10 AM
exactly. this activity-cohort answers engagement/usage retention. NRR (nrr_trailing_12) answers revenue retention on a fixed paid cohort with churned-at-$0. don't confuse the two — they answer different questions and will give different numbers. for the board, NRR. for product/usage analysis, activity cohorts.

**newgrad.sam** — 10:12 AM
got it. activity cohort = usage stickiness, NRR = revenue retention. different tools. and NRR keeps churned in at $0, this activity one just naturally shows them as not-active (no event rows).

**nina.patel** — 10:14 AM
right. ty for connecting it. the cohort glossary (`glossary__cohort.md`) has more on the distinction if you want it.

---

# #random — 2025-11-26 — thanksgiving eve

**marco.silva** — 3:00 PM
half the office is already on PTO, the other half is pretending to work, it's thanksgiving eve and productivity has left the building

**grace.liu** — 3:02 PM
I'm "working from home" which means the kiln is on and I'm checking Slack between glaze coats

**david.kim** — 3:03 PM
honest. I'm "reviewing PRs" which means I have a PR open in a tab while I plan my turkey brine

**yuki.sato** — 3:10 PM
the EMEA office is fully operational and slightly resentful, enjoy your bird

**marco.silva** — 3:11 PM
we'll save you a metaphorical drumstick yuki

---


#data-help — 2025-12-02

**lina.cho** — 9:15 AM
Hey @rajiv.menon — I’m trying to reconcile the Q4 NRR numbers for the board deck and I'm seeing a discrepancy between my manual calc and the `nrr_trailing_12` mart. 

My query:
```sql
SELECT 
  SUM(prev.mrr_usd) as cohort_start_mrr,
  SUM(curr.mrr_usd) as cohort_end_mrr,
  SUM(curr.mrr_usd) / SUM(prev.mrr_usd) as nrr
FROM `nexus-analyst-demo.acme.fact_subscriptions` prev
JOIN `nexus-analyst-demo.acme.fact_subscriptions` curr 
  ON prev.customer_id = curr.customer_id
WHERE prev.is_current = FALSE 
  AND prev.end_date = '2024-12-01'
  AND curr.is_current = TRUE
```
I'm getting 1.18 but the mart says ~1.07. Why is the mart so much lower?

**rajiv.menon** — 9:22 AM
@lina.cho you're using an `INNER JOIN`. That’s the classic trap. You’re only looking at customers who are *still* customers today. You’re dropping everyone who churned in the last 12 months, which obviously inflates the number. 

The canonical NRR calculation (and what’s in `acme.nrr_trailing_12`) needs to include those churned accounts at $0.

**nina.patel** — 9:25 AM
Exactly. Use `LEFT JOIN` and `COALESCE(curr.mrr_usd, 0)`. If they downgraded to the Free plan, they also count as $0 for NRR purposes. The board NRR is fixed-cohort. 

**lina.cho** — 9:28 AM
Ah, right. Churned-at-zero. Let me re-run. Is the mart updated for the Cobalt Systems (cust_000700) expansion yet? They just bumped to 80 seats.

**rajiv.menon** — 9:30 AM
dbt runs every morning at 6am. If it happened yesterday, it's in `arr_snapshot` and `nrr_trailing_12` now. Also, reminder: don't try to query `acme.marts.finance.nrr_trailing_12` — I saw some old documentation floating around with that path. BigQuery is flat: `nexus-analyst-demo.acme.nrr_trailing_12`. 

---

# #random — 2025-12-04

**marco.silva** — 11:45 AM
Who left the half-eaten tuna melt in the SF office micro-kitchen? The humidity in there is making it... sentient.

**grace.liu** — 11:47 AM
not me, i'm a salad person today.

**david.kim** — 11:48 AM
it's been there since the workshop on Tuesday. I've named it "The Integration".

**sarah.chen** — 11:50 AM
Can we please get a Slack bot for fridge cleanouts? Or just more LaCroix? We’re out of Pamplemousse again.

**sam.reyes** — 12:05 PM
I'll ping Ops about the Pamplemousse. Also, if "The Integration" starts answering support tickets, let me know, we might be able to headcount-shift.

---

# #data-help — 2025-12-08

**omar.haddad** — 2:15 PM
Trying to pull a list of "Engaged" customers for the APAC quarterly review. Is the definition still "anyone with a login"?

**nina.patel** — 2:18 PM
Nope, we tightened that up in Q4. A login isn't enough anymore. 
An "Engaged" customer = 
1. At least 3 active users in the last 28 days.
2. At least 10 successful workflow runs in the last 28 days.

Check `acme.account_health`. There's a boolean column `is_engaged` that handles this logic so you don't have to keep joining `fact_user_events` and `fact_workflow_runs`.

**omar.haddad** — 2:22 PM
Thanks Nina. Quick follow up—I see a `vrs_band` column in a draft doc for the `account_health` table. I'm trying to query it but getting a "column not found" error. 

**nina.patel** — 2:25 PM
Ignore that doc. The Value Realization Score (VRS) is a parked spec. We never built the champion login recency logic into the warehouse. Stick to `is_engaged` and `utilization_band` for now.

**omar.haddad** — 2:30 PM
Got it. Also, looking at Onyx Robotics (cust_000704). They show as `critical` in the health mart, but they have 500 seats and are definitely using it. Is the utilization logic broken for Enterprise?

**nina.patel** — 2:34 PM
Enterprise `critical` is different. They don't have a utilization threshold because they have unlimited seats/runs often. For Enterprise, `critical` ONLY triggers if they have a recent uncollectible invoice. Check `fact_invoices` for cust_000704 — they might have a payment failing.

---

# #sales-ops — 2025-12-10

**jorge.martinez** — 10:00 AM
@tom.becker — did you log the Ember Industries (cust_000711) expansion in the CRM? I'm not seeing it in the `bookings_attribution` mart.

**tom.becker** — 10:05 AM
Just did it 20 mins ago. 350 seats, $25k MRR. 

**jorge.martinez** — 10:07 AM
Cool. Remember, for the bookings report, `bookings_acv_usd` is already annualized in the warehouse. Don't multiply it by 12 when you're doing your local Excel sheets or it'll look like we hit our annual target in a week. (I wish).

**sarah.chen** — 10:10 AM
Wait, does `bookings_attribution` include the self-serve Pro upgrades? I have a few of those from Marigold Health (cust_000701) users who just swiped a card.

**jorge.martinez** — 10:12 AM
No. `bookings_attribution` is only for AE-led deals (Business/Enterprise). Self-serve Free -> Pro conversions don't create an Opportunity in the CRM, so they don't show up there. You have to look at `fact_subscriptions` for the `change_type = 'upgrade'` events for those.

---

# #data-help — 2025-12-12

**david.kim** — 4:00 PM
Debugging a weird error in `fact_workflow_runs`. Seeing a spike in `error_code = 'INTEGRATION_DOWN'` for EMEA customers this afternoon.

```sql
SELECT 
  customer_id, 
  COUNT(*) as fail_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE error_code = 'INTEGRATION_DOWN'
  AND triggered_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 4 HOUR)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;
```
Top one is Tamarind Group (cust_000706). Oh wait, they’re paused. 

**nina.patel** — 4:05 PM
Tamarind is `status = 'paused'` as of Jan 2026 (wait, checking the dim... yeah). They shouldn't be running workflows at all.

**david.kim** — 4:07 PM
My bad, I was looking at an old export. But yeah, the spike is real. Mostly `fintech` industry customers in EMEA. Cobalt Systems (cust_000700) and Sable Analytics (cust_000710) are both hitting it. Might be a regional API outage for one of the banks we connect to.

**nina.patel** — 4:10 PM
I’ll check the `integration_down_count` in `workflow_runs_daily`. If it’s high, we need to alert Marco, he’s the CSM for both of those.

---

# #random — 2025-12-15

**yuki.sato** — 9:00 AM
The Amsterdam office is having a "Speculaas and Code" morning. If anyone wants to join the Zoom, we’re mostly just eating cookies and debating whether `is_business_day` in `dim_dates` should account for regional holidays or just weekends.

**rajiv.menon** — 9:05 AM
Regional holidays please! My Dutch pipeline reports always look weird on King's Day.

**olivia.tran** — 9:10 AM
+1. APAC holidays too. Verdant Cloud (cust_000707) always has zero runs during Lunar New Year and it triggers my "at_risk" alerts every time.

**nina.patel** — 9:12 AM
I can add a `country_code` join to `dim_dates` but it’s going to make that table huge. Let’s keep it to weekends for the canonical version and you guys can overlay the holiday calendars in Looker.

---

# #product-updates — 2025-12-18

**dan.lee** — 11:00 AM
Heads up everyone: we’re moving the audit log feature from the Pro tier to the Business tier starting Jan 1st. 
Existing Pro customers like Driftwood Media (cust_000702) will be grandfathered for 6 months.

**elena.volkov** — 11:05 AM
This is going to be a fun conversation for the CSMs. @grace.liu — can you pull a list of Pro customers using audit logs more than once a week? 

**grace.liu** — 11:10 AM
On it. I'll check `fact_user_events` for `event_name = 'audit_log_exported'`.

```sql
SELECT 
  c.customer_id,
  c.company_name,
  COUNT(e.event_id) as export_count
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_user_events` e ON c.customer_id = e.customer_id
WHERE c.current_plan_tier = 'Pro'
  AND e.event_name = 'audit_log_exported'
  AND e.event_at > '2025-11-01'
GROUP BY 1, 2
HAVING export_count > 4;
```
Pebble Digital (cust_000705) and Willow Works (cust_000709) are the heavy hitters here. They’re basically using Pro but need Business-level compliance. Good expansion targets for Sarah and Yuki.

---

# #data-help — 2025-12-20

**rajiv.menon** — 3:00 PM
Final reminder for EOY reporting: 
- Total ARR is roughly $39M. 
- Business tier is the bulk (~$32M). 
- Enterprise is ~$6M.
- Pro is ~$1M.
If your numbers don't match this, check your `fact_subscriptions` filters. You MUST filter for `is_current = TRUE` and `plan_tier != 'Free'`. 

If you use `dim_customers.current_mrr_usd`, it might be slightly off due to the intraday refresh lag (BI lags prod by 2h). `arr_snapshot` is the only source for board-level "Truth".

**lina.cho** — 3:05 PM
Thanks Rajiv. Quick check: does the Enterprise ARR include the custom SLA credits we gave to Marigold Health (cust_000701) last month?

**rajiv.menon** — 3:10 PM
No, ARR is gross contracted revenue. The credits show up in `fact_invoices` as a reduction in `amount_usd`, but they don't touch the MRR/ARR in the subscription table. We keep the top-line clean.

**lina.cho** — 3:15 PM
Wait, @rajiv.menon if `arr_snapshot` is the "Truth", why does my NRR (Net Revenue Retention) calc for November look like 114% when Finance is reporting 108%? 

I’m joining `fact_subscriptions` to itself to find the delta:

```sql
WITH mrr_mo AS (
  SELECT 
    customer_id,
    date_trunc(start_date, MONTH) as mo,
    SUM(mrr_usd) as total_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE is_current = TRUE -- Is this the problem?
  GROUP BY 1, 2
)
SELECT 
  curr.mo,
  SUM(curr.total_mrr) / NULLIF(SUM(prev.total_mrr), 0) as nrr
FROM mrr_mo curr
LEFT JOIN mrr_mo prev ON curr.customer_id = prev.customer_id 
  AND curr.mo = DATE_ADD(prev.mo, INTERVAL 1 MONTH)
GROUP BY 1;
```

**rajiv.menon** — 3:22 PM
`is_current = TRUE` is definitely the problem there. That flag only shows the *active* state right now. For historical NRR, you can't use `is_current`. You need to look at the `start_date` and `end_date` ranges for each subscription record. 

Also, check if you’re including the expansion from Pebble Digital (cust_000705) correctly—they added 40 seats in mid-November but the `change_type` was logged as 'seat_increase', not 'renewal'.

**grace.liu** — 3:25 PM
Lina, try using `nexus-analyst-demo.acme.fact_subscriptions` but filter where the month in question falls BETWEEN `start_date` and `end_date`. If `end_date` is null, it’s still active. 

And don't forget the 'Churn' records. If a customer is in `prev` but not `curr`, they should be 0, not NULL.

---

# #random — 2025-12-21

**marcus.thorn** — 9:15 AM
Who left the half-eaten oat milk latte next to the MicroKitchen printer? It’s growing a civilization. 

**yuki.tanaka** — 9:20 AM
Not mine. I’m a matcha person. 🍵 
Also, did we ever decide on the holiday off-site? Or is the "automation" of our social lives just more Zoom calls?

**dan.lee** — 9:45 AM
@yuki.tanaka Engineering is doing a hackathon on the 27th, but most of CS is taking the week. 
Speaking of, is anyone else seeing weird latency on the VRS (Vault Reporting System)? I’m trying to pull the Q4 bookings for the Marigold Health (cust_000701) expansion and it’s timing out.

---

# #data-help — 2025-12-22

**sarah.jenkins** — 10:05 AM
Can someone help me define "Active Customer" for the Q4 Business Review? 
Is it just anyone with an active subscription, or do they actually have to be *using* the platform? 

**elena.volkov** — 10:10 AM
Product definition is: >= 5 successful `fact_workflow_runs` in the last 30 days. 
If they just log in but don't run any workflows, they’re "Zombie accounts." 

**grace.liu** — 10:15 AM
@sarah.jenkins here is the snippet I use for the "Healthy Active" metric. 

```sql
SELECT 
    c.customer_id,
    c.company_name,
    COUNT(r.run_id) as total_runs
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
WHERE r.triggered_at >= CURRENT_DATE() - 30
  AND r.status = 'success'
  AND c.status = 'Active'
GROUP BY 1, 2
HAVING total_runs >= 5;
```
Note: Willow Works (cust_000709) has a ton of runs but most are `error_code = 'AUTH_FAIL'`. They might look active but their integration is actually broken. Check `fact_workflow_runs.error_code`.

**sarah.jenkins** — 10:20 AM
Thanks Grace! That explains why Willow Works keeps pinging me about their "usage" being high. They're just hitting a loop.

**rajiv.menon** — 10:45 AM
@here PSA: I am running a backfill on `dim_users` to fix the `email_domain` column. It was incorrectly stripping the subdomains for some of our Enterprise accounts (like `uk.marigoldhealth.com` becoming just `health.com`). 
Table will be locked for ~10 mins. 

**lina.cho** — 10:50 AM
While you're in there, can you check why `dim_customers.acquisition_channel` is NULL for Driftwood Media? They were a referral from the Q2 webinar but it looks like the attribution got lost when they upgraded from Pro to Business.

**rajiv.menon** — 10:55 AM
Ack. It's because the upgrade created a new `customer_id` in the old legacy CRM before we migrated to the unified flat schema. I'll manually patch it to 'Marketing - Webinar'. 

---

# #eng-status — 2025-12-23

**dan.lee** — 9:00 AM
Standup in 5. 
Updates:
- Audit log migration to Business tier is 90% coded. 
- API rate limiting for Free tier customers (100 runs/mo) is now strictly enforced. 
- @elena.volkov — we need to talk about the `step_count` in `fact_workflow_runs`. Some users are building 200+ step workflows and it’s killing the worker nodes. We might need a hard cap for Pro users.

**elena.volkov** — 9:05 AM
Let’s cap Pro at 50 steps per workflow. Business and Enterprise can stay unlimited for now. 
Check the `fact_workflow_runs` for anything where `step_count > 100`—I bet it's mostly Pebble Digital (cust_000705). They’re basically using us as a database ETL tool.

**dan.lee** — 9:10 AM
```sql
SELECT 
    c.company_name,
    r.workflow_id,
    MAX(r.step_count) as max_steps
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE r.triggered_at > '2025-12-01'
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;
```
Yep. Pebble is at 245 steps. Also seeing some high numbers from a few Free tier users trying to bypass the run quota by doing everything in one giant execution. Clever, but no.

---

# #random — 2026-01-05

**marcus.hopkins** — 8:45 AM
SF Office: The espresso machine on the 4th floor is leaking again. Avoid the area unless you want wet socks. I’ve put a ticket in with Building Ops. ☕️🚫

**sarah.chen** — 8:50 AM
Again?? That’s the third time since the Series B party. We should just buy a commercial-grade one at this point. 

**rajiv.menon** — 9:12 AM
If we hit our NRR targets for Q1, maybe finance will let us expense a La Marzocco. Speaking of NRR, @sarah.chen did you see my note about the `fact_subscriptions` join?

**sarah.chen** — 9:15 AM
Checking it now.

---

# #data-help — 2026-01-05

**sarah.chen** — 9:20 AM
Hey @rajiv.menon — I’m trying to pull NRR for the Board Deck but my numbers look insane (like 210% for the Mid-Market segment). I think I’m double-counting the upgrades when a customer moves from Pro to Business mid-month.

I’m using:
```sql
SELECT 
    date_trunc(s.start_date, MONTH) as month,
    c.account_tier,
    SUM(s.mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
WHERE s.is_current = true
GROUP BY 1, 2
```
But this only gives me a point-in-time snapshot, right? How do I get the "Beginning of Month" MRR for customers who were active 12 months ago?

**rajiv.menon** — 9:35 AM
Yeah, `is_current = true` will only show you the *now*. You need to look at the `change_type` column in `fact_subscriptions`. 

For NRR, you want:
(Beginning MRR + Expansion + Resurrections - Contraction - Churn) / Beginning MRR.

Try joining the table to itself with a `date_add(month, INTERVAL -1 YEAR)` logic. Also, watch out for the `customer_id` vs `subscription_id`. Some legacy accounts have multiple `subscription_id` rows for the same period because of that weird billing bug in late 2024.

**lina.cho** — 10:05 AM
@sarah.chen also, make sure you filter out the `Free` tier. Their MRR is 0 but they show up in `dim_customers` and can skew the account counts if you’re doing NRR on a per-customer basis rather than pure dollars.

**sarah.chen** — 10:15 AM
Got it. Does `dim_customers.status = 'active'` include `paused` accounts? 

**rajiv.menon** — 10:20 AM
No, `paused` is its own status. We only have about 10 of those (mostly seasonal Enterprise folks like Marigold Health when they do their off-cycle audits). For NRR, treat `paused` as contraction MRR if their spend goes to $0, but don't mark them as `churned` or you'll mess up the retention cohorts.

---

# #eng-status — 2026-01-06

**dan.lee** — 9:02 AM
VRS (Virtual Run Service) is seeing some latency spikes in the EMEA region (Amsterdam cluster). 
@elena.volkov — seeing a lot of `error_code: 504` in `fact_workflow_runs` for customers in `region = 'EMEA'`. 

**elena.volkov** — 9:10 AM
Looking at the logs. It's the webhook listener. It looks like a specific customer is flooding us. 
Let me check the warehouse...

```sql
SELECT 
    c.company_name,
    COUNT(*) as run_count,
    AVG(duration_ms) as avg_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE r.triggered_at > timestamp_sub(current_timestamp(), INTERVAL 2 HOUR)
  AND r.status = 'error'
GROUP BY 1
ORDER BY 2 DESC
```

**elena.volkov** — 9:15 AM
It's `cust_000124` (Alpha Logistics). They’re on a Business plan but they’ve triggered 45,000 runs in the last hour. Our rate limiter for Business is set at 100k/month, but they’re hitting the *burst* limit. 

**dan.lee** — 9:18 AM
Alpha Logistics is one of @marcus.hopkins' accounts. Marcus, can you tell them to throttle their webhook sender? Or we can bump them to a temporary Enterprise "Unlimited" bucket if they want to pay for the overage.

**marcus.hopkins** — 9:25 AM
On it. They’re migrating their legacy ERP to the cloud this week, so this is probably a one-time sync. I'll see if they’ll bite on an Enterprise upgrade for the "dedicated priority queue" feature.

---

# #data-help — 2026-01-07

**nina.vargas** — 2:30 PM
Quick question for the analysts: Why does `dim_employees.is_active` show as `false` for me in the latest dbt run? I am very much still here and drinking the mediocre coffee. 😅

**rajiv.menon** — 2:35 PM
Whoops. @nina.vargas — it looks like the HR export from Workday had a typo in your `termination_date` (it was set to 2026-01-01 instead of null). I’ll manually override the `dim_employees` mart and push a fix to the source sheet. 

**lina.cho** — 2:40 PM
While you're fixing Nina, can you check the `ae_employee_id` in `dim_customers`? There are about 50 accounts where it’s `NULL` but they are clearly `account_tier = 'MM'` or `'Ent'`. 

Specifically:
- `cust_000882` (Bluebird Financial)
- `cust_000890` (Oak & Iron)

They both signed in Dec 2025.

**rajiv.menon** — 2:50 PM
Ah, those were the "Inbound Fast-Track" deals. They skipped the SDR qualification and went straight to a "House Account" because we didn't have an AE assigned during the holiday break. I'll assign them to the Sales Manager (Employee `emp_002`) for now in the flat table. 

---

# #ops-general — 2026-01-08

**sarah.chen** — 11:00 AM
Does anyone have the canonical definition for "Active User" (WAU)? 
Is it `last_login_date` within 7 days, or do they have to actually trigger a workflow run in `fact_workflow_runs`? 

**lina.cho** — 11:05 AM
Product defines WAU as "at least one event in `fact_user_events` where `event_type` is NOT 'login' within the last 7 days." 
Just logging in doesn't count as "active engagement" per the Q4 Board Deck. 

**sarah.chen** — 11:10 AM
That's going to drop our WAU/MAU ratio by like 15%. 

**lina.cho** — 11:12 AM
Yep. But it’s more honest. We have a lot of "Ghost Admins" who log in once a month to check the billing page but never actually build anything. 

**dan.lee** — 11:15 AM
If you're writing that query, use the `nexus-analyst-demo.acme.fact_user_events` table. It’s partitioned by `event_at`, so it’ll be much cheaper than scanning the whole `dim_users` table for `last_login_date`.

```sql
-- Example WAU query
SELECT 
    count(distinct user_id) 
FROM `nexus-analyst-demo.acme.fact_user_events`
WHERE event_at >= timestamp_sub(current_timestamp(), INTERVAL 7 DAY)
  AND event_type NOT IN ('login', 'logout')
```

**sarah.chen** — 11:20 AM
Thanks Dan. Also, lunch at The Sentinel today? I need a sandwich.

**dan.lee** — 11:21 AM
12:15. I'm in. 🥪

---

# #data-help — 2026-01-09

**marcus.hopkins** — 4:00 PM
Trying to calculate "Time to Value" for the Q1 cohort. I’m looking for the delta between `signup_date` in `dim_customers` and the first `SUCCESS` status in `fact_workflow_runs`. 

Has anyone already built a view for this?

**rajiv.menon** — 4:10 PM
Check `fct_customer_first_success`. It’s a hidden mart I built for the CS team. 
Path: `nexus-analyst-demo.acme.fact_customer_milestones` (I consolidated a few of those first-event facts there).

Look for `milestone_name = 'first_successful_run'`. 

Warning: For some of the older 2023 accounts, the `fact_workflow_runs` history is patchy because we weren't logging the `step_count` correctly, so some rows might be missing if the run was super short.

**marcus.hopkins** — 4:15 PM
Found it. Thanks! 
Wait, why does `Driftwood Media` have a `signup_date` of 2025-06-01 but their first success is 2025-05-15? Did they use the product before they signed up?

**lina.cho** — 4:18 PM
@marcus.hopkins — They were part of the Beta for the "Shared Workspaces" feature. They had a `Free` account under a different `customer_id` that got merged when they upgraded to the Business tier. The `signup_date` in `dim_customers` usually reflects the *current* contract start date for upgrades, not the original PLG entry date. 

It’s a known issue. We’re working on a `dim_account_lineage` table to track these merges but it’s a mess. 

**marcus.hopkins** — 4:20 PM
Data is hard. See you all at the standup. 

---

# #data-help — 2026-01-12

**jessica.mora** — 9:15 AM
Hey team, I'm trying to pull the Q4 2025 New Logo Bookings report for the Board. I’m looking at `nexus-analyst-demo.acme.fact_subscriptions` and filtering by `change_type = 'new_customer'`. 

My total is coming up about $12k short of what Sales Ops has in Salesforce for `Solaris Tech`. Anyone know if there’s a lag?

**rajiv.menon** — 9:22 AM
@jessica.mora Check the `start_date`. Solaris Tech signed on 2025-12-30, but their provisioning didn't actually finish until 2026-01-02. 

Our BQ sync for `fact_subscriptions` only records the row once the status is active in the billing system. If the invoice is still 'Pending' or 'Draft' in Stripe, it won't hit the flat table yet. 

**jessica.mora** — 9:25 AM
Ah, okay. So it’s a timing difference between the SFDC "Closed Won" date and the actual subscription start. 

Wait—I also see `Papercut Industries` listed with an `mrr_usd` of $4,166. They signed a $50k Enterprise deal. Why is the MRR so low?

**lina.cho** — 9:28 AM
@jessica.mora $50,000 / 12 months = $4,166.66. 

The `fact_subscriptions` table always normalizes to monthly revenue (MRR), even for annual Enterprise contracts. If you want the TCV (Total Contract Value) for the bookings report, you need to multiply `mrr_usd` by 12 or pull from the `fact_invoices` table where `period_start` and `period_end` show the full year. 

**jessica.mora** — 9:30 AM
Got it. I'll just annualize the MRR for the bookings deck. Thanks Lina!

---

# #random — 2026-01-12

**dan.lee** — 10:05 AM
Whoever left the half-eaten avocado toast in the 3rd floor fridge... please. It’s a biohazard at this point. 🥑🤢

**sarah.chen** — 10:10 AM
Not me, I’m a strictly "Sentinel sandwich" person today. 

**marcus.hopkins** — 10:11 AM
Speaking of, anyone heading to Philz in 10 mins? I need caffeine to deal with this NRR spreadsheet.

---

# #data-help — 2026-01-14

**marcus.hopkins** — 2:10 PM
I am losing my mind. I'm trying to calculate Net Revenue Retention (NRR) for the MM (Mid-Market) segment for Jan 2026. 

Querying `nexus-analyst-demo.acme.fact_subscriptions` and joining `dim_customers`. 
My NRR is coming out to 145% which feels... too good to be true? Even for us. 

**lina.cho** — 2:15 PM
@marcus.hopkins You’re probably double-counting the upgrades. 

Are you filtering for `is_current = TRUE`? If you just sum `mrr_usd` for a customer without filtering for the specific timestamp, you’ll get their *old* plan and their *new* plan added together if they upgraded during the month. 

**marcus.hopkins** — 2:20 PM
I was using `is_current`. 
Wait, I see the issue. I'm joining on `customer_id` but some customers have multiple subscriptions for different departments (the "Land and Expand" motion). 

If `Global Corp` has a Pro sub for Marketing and a Business sub for Ops, they show up twice.

**rajiv.menon** — 2:22 PM
Marcus, use the `dim_customers.current_mrr_usd` field if you just want a snapshot of today. 

If you're doing historical NRR, you have to use `fact_subscriptions` but you need to group by `customer_id` and `date_trunc(start_date, MONTH)` first to collapse those multi-sub accounts. 

Also, watch out for `status = 'paused'`. We still count them as "active" customers in `dim_customers` but their `mrr_usd` drops to $0. It’ll tank your retention numbers if you don't handle the nulls.

**marcus.hopkins** — 2:35 PM
Okay, updated the join. Now I'm at 112%. That looks way more realistic. 
Quick check: Does `account_tier` in `dim_customers` update historically? 

**lina.cho** — 2:40 PM
No, `dim_customers` is a Type 1 dimension right now (overwrites). If an SMB account grew into MM last week, it shows as MM for their entire history in that table. 

If you need the tier they *were* at on Jan 1st, you have to look at `seat_count` in `fact_subscriptions` for that date. 
0-49 seats = SMB
50-249 = MM
250+ = Ent

**marcus.hopkins** — 2:42 PM
"Data is hard" — Me, every Tuesday. Thanks all.

---

# #data-help — 2026-01-15

**sarah.chen** — 11:00 AM
Is the VRS (Validation Reporting Service) down? My Looker dashboard for `Workflow Success Rates` hasn't refreshed since 4 AM. 

**dan.lee** — 11:05 AM
Checking the logs... 
Yeah, looks like the `fact_workflow_runs` load failed because of a schema change in the upstream webhook logs. Someone added a `retry_count` field as a string instead of an int. 

I’m re-running the dbt pipeline now. Should be green in 20 mins. 

**sarah.chen** — 11:06 AM
Thanks Dan. I have a 11:30 with the VP of Product, so hopefully it’s back by then. 

**dan.lee** — 11:25 AM
Pipeline finished. Looker should be fresh. 

Note for everyone: Please use the **FLAT** tables in `nexus-analyst-demo.acme`. Stop trying to query the `stg_` or `base_` folders in the warehouse. We’re deprecating those next month and the permissions are going to get restricted. 

If it doesn't start with `dim_` or `fact_`, don't use it for reporting!

**rajiv.menon** — 11:26 AM
+1. I still see someone running queries against `nexus-analyst-demo.acme.raw_logs_events`. That table is 4TB. You are going to blow our BigQuery budget for the quarter in one afternoon. Use `fact_user_events`! It’s partitioned!

**marcus.hopkins** — 11:28 AM
Guilty. 🙋‍♂️ Sorry Rajiv, I was looking for a specific `error_code` that wasn't in the fact table yet. I'll be good, I promise. 🌯 lunch on me?

# #data-help — 2026-01-22

**marcus.hopkins** — 9:15 AM
Hey team, I'm trying to pull NRR (Net Retention Rate) for the Q4 cohort of MM customers. I'm getting 142% which seems... suspiciously high? Even for us. 

I’m joining `dim_customers` to `fact_subscriptions` on `customer_id`. 

**lina.cho** — 9:20 AM
@marcus.hopkins check your join logic on `fact_subscriptions`. Are you filtering for `is_current = true`? If you just join on `customer_id`, you’re going to get every historical row for every seat change or plan upgrade that happened in Q4. You're likely triple-counting the MRR for accounts that expanded.

**marcus.hopkins** — 9:22 AM
Ah, yep. That’s it. I see 4 rows for "Global Logistics Corp" because they added seats three times in November. 🤦‍♂️

**rajiv.menon** — 9:25 AM
Also Marcus, remember that `mrr_usd` in `fact_subscriptions` is the *snapshot* value for that specific record. If you want the delta (expansion vs new biz), you need to compare `mrr_usd` to the `changed_from_subscription_id` record. 

Or just use the `marts_finance.fct_mrr_movements` table if you don't want to do the math yourself. Oh wait, you guys don't have access to the `marts_` schema yet. Stick to the FLAT tables.

**marcus.hopkins** — 9:30 AM
Is there a flat version of the MRR movements table? 

**dan.lee** — 9:32 AM
Not yet. It’s on the sprint for next week. For now, you have to do the lag function over `fact_subscriptions` partitioned by `customer_id` ordered by `start_date`. 

**marcus.hopkins** — 9:35 AM
"Lag function" is my trigger word. I'll just wait for the mart. 😂 
Actually, I'll try the join again with `is_current`. Thanks Lina.

---

# #random — 2026-01-23

**rajiv.menon** — 10:05 AM
Is the espresso machine in the SF office 3rd floor lounge broken again? It’s making a sound like a 1990s dial-up modem. 

**sarah.chen** — 10:10 AM
It's not broken, it's "character." But yeah, I put a ticket in with Ops. Use the one on 4 for now.

**dan.lee** — 10:12 AM
The one on 4 is out of beans. 

**rajiv.menon** — 10:13 AM
This is a P0. Someone update the status page.

---

# #data-help — 2026-01-24

**sarah.chen** — 2:15 PM
Question for the group: What is our official "Active User" definition for the Board deck? I see two different numbers in the `Engagement_Overview` dashboard. 

**lina.cho** — 2:20 PM
Depends on who you ask. 
Product (Growth) uses: 1+ login in 28 days.
Engineering uses: 1+ `workflow_run` triggered in 30 days.

We usually report the "WAU" (Weekly Active Users) as anyone who triggered a successful run in the last 7 days. Look at `nexus-analyst-demo.acme.fact_user_events` where `event_type = 'workflow_triggered'`.

**sarah.chen** — 2:25 PM
Okay, because I’m looking at `dim_users` and the `last_login_date` count is way higher than the run count. 

**rajiv.menon** — 2:27 PM
That makes sense. A lot of users at our Enterprise customers (like "DataDynamics" or "FinTech Solutions") login just to check the audit logs or update the SSO settings but never actually build/run a workflow. 

If you want "Engagement," use the run counts. If you want "Footfall," use the login dates. 

**sarah.chen** — 2:30 PM
I’ll stick with the 28d active run count. It feels more honest. 
Wait, why does `fact_workflow_runs` have `customer_id` but not `user_id` for some rows?

**dan.lee** — 2:32 PM
Those are scheduled runs or webhook triggers. There's no "user" physically clicking a button, so `triggered_by` is 'SYSTEM'. 

If you filter `triggered_by != 'SYSTEM'`, you'll get the manual/UI-initiated runs linked to a specific `user_id`. 

---

# #data-help — 2026-01-26

**marcus.hopkins** — 11:45 AM
Quick check—I'm looking at `nexus-analyst-demo.acme.dim_customers` for "CloudScale Inc". 
It says `account_tier` is 'SMB' but their `current_mrr_usd` is $4,500. 
Doesn't the Business plan (which starts at 50 seats) put them in MM? 

**lina.cho** — 11:50 AM
CloudScale is a legacy account from early 2024. They’re on a "Pro" plan with a huge number of seats because they got a grandfathered rate. 

Tiering logic is based on seat count *at the time of the last renewal*, not just MRR. 
- SMB: < 50 seats
- MM: 50-249 seats
- Ent: 250+ 

If they have 48 seats but are paying a lot because of usage overages (which aren't in the flat tables yet, btw), they still show as SMB.

**marcus.hopkins** — 11:55 AM
Got it. So `seat_count_licensed` is the source of truth for the tier, not the revenue. 

**rajiv.menon** — 11:58 AM
Correct. We’re actually planning to move to revenue-based tiering in FY27 because of exactly this confusion. For now, trust the seat counts in `fact_subscriptions`.

**marcus.hopkins** — 12:00 PM
By the way, who is the AE for "BioGen Research"? The `ae_employee_id` in `dim_customers` is null. 

**dan.lee** — 12:05 PM
They signed up via the Pro self-serve flow last month and haven't talked to a human yet. Any customer with `acquisition_channel = 'PLG'` won't have an AE assigned until they hit the 50-seat threshold and trigger a MQL for the sales team. 

**marcus.hopkins** — 12:06 PM
Cool, thanks Dan. Heading to lunch. 🌮 Anyone want anything?

**dan.lee** — 12:07 PM
Burrito. No cilantro. 

**rajiv.menon** — 12:08 PM
+1 on the burrito. Extra cilantro. Balance out Dan.

---

# #data-help — 2026-01-27

**sarah.chen** — 9:00 AM
VRS check? My "Workflow Success by Industry" chart is showing 0% for everything yesterday. 

**dan.lee** — 9:15 AM
Checking... 
Looks like the `fact_workflow_runs` update hung because BigQuery had a transient error on the partition overwrite. I’m re-running the job for the 2026-01-26 partition now. 

Give it 15 minutes. 

**sarah.chen** — 9:16 AM
Is this going to affect the `daily_usage_summary` for the EMEA accounts too?

**dan.lee** — 9:20 AM
Yeah, anything downstream of `fact_workflow_runs`. 
Actually, while I'm in here, does anyone know why we have 2,000 runs for `customer_id` 'CUST-9999'? That's the internal test account, right? 

**rajiv.menon** — 9:22 AM
Yeah, that's the QA team's stress test bot. I usually filter that out of my queries: 
`WHERE customer_id NOT LIKE 'CUST-999%'` 

If you don't, it'll skew your average `duration_ms` because those test workflows are basically empty and run in like 50ms. 

**sarah.chen** — 9:25 AM
That explains why my 'Tech' industry average duration plummeted. Thanks Rajiv. 

**dan.lee** — 9:45 AM
Job's done. Tables are fresh. Go wild.

# #data-help — 2026-01-28

**marcus.hopkins** — 10:15 AM
Quick sanity check on NRR for the Board deck. I’m getting 118% for the Business tier in Q4, but Finance is reporting 112%. 

Here is my query: 
```sql
SELECT 
  sum(mrr_usd) 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current = true 
  AND plan_tier = 'Business'
```
Am I missing a filter?

**rajiv.menon** — 10:22 AM
Yeah, NRR needs to be cohort-based, Marcus. You're just looking at current MRR. To get NRR, you need to compare the MRR from the *same* group of customers as they were 12 months ago. 

Also, check if you're including `change_type = 'new_logo'` in your numerator. You shouldn't. NRR is purely expansion, contraction, and churn of the base that existed at the start of the period. 

**dan.lee** — 10:25 AM
@marcus.hopkins also make sure you're joining on `customer_id` and not `subscription_id`. If a customer upgraded from Pro to Business, they get a new `subscription_id` but keep the same `customer_id`. If you join on sub ID, you'll lose the history.

**marcus.hopkins** — 10:30 AM
Ah, the Pro -> Business jump is definitely what's messing me up. 🤦‍♂️

**sarah.chen** — 10:32 AM
Marcus, I have a pre-baked view for this: `mart_finance.net_revenue_retention`. It handles the 12-month lookback logic and filters out the PLG-to-Enterprise conversions correctly. 

**marcus.hopkins** — 10:35 AM
Is that using the FLAT schema or the legacy nested one?

**sarah.chen** — 10:36 AM
Everything in `mart_finance` is pointed at the `nexus-analyst-demo.acme` FLAT tables now. We deprecated the nested stuff back in November. 

**marcus.hopkins** — 10:37 AM
Perfect. Saved me an hour of debugging joins. 

---

# #random — 2026-01-29

**dan.lee** — 8:45 AM
The espresso machine in the 4th floor micro-kitchen is leaking again. Please don't use it unless you want a soggy shoes day. ☕️🚫

**rajiv.menon** — 8:50 AM
Again? That’s the third time this month. I’m putting in a Jira ticket for Facilities. 

**sarah.chen** — 9:02 AM
"Espresso Machine Leak" — Priority: P0 (Blocker) 

---

# #data-help — 2026-01-30

**sarah.chen** — 11:00 AM
Does anyone know why `dim_customers.seat_count_licensed` is lower than the actual count in `fact_user_events` for "Cyberdyne Systems"? 

They are licensed for 150 seats but I see 162 unique `user_id`s firing `workflow_executed` events in the last 7 days. 

**dan.lee** — 11:15 AM
That usually means they’re over-provisioned. Our SSO sync doesn't hard-block new users if they exceed the license count; it just flags it for the CSM. 

Check `dim_customers.csm_employee_id`. Who’s the lead on Cyberdyne? 

**sarah.chen** — 11:17 AM
It's `EMP-442`... let me check `dim_employees`... that's Maria Garcia. 

**dan.lee** — 11:20 AM
Yeah, Maria usually lets the overage run for a month before hitting them with an expansion invoice. It's a "land and expand" tactic. 

If you want the "true" billable count, always use `fact_subscriptions.seat_count` where `is_current = true`. The `dim_users` table will always show everyone who has ever logged in, even if they aren't technically "paid for" yet. 

**sarah.chen** — 11:22 AM
Got it. I'm trying to build a "Seat Utilization" heat map. 

`utilization_rate = (active_users_last_30d / seat_count_licensed)`

If it's > 100%, I'll flag it as an expansion opportunity for Sales.

**rajiv.menon** — 11:25 AM
Careful with `active_users_last_30d`. Use `fact_user_events` and filter for `event_type = 'login'` or `workflow_run`. Sometimes people are "active" in the metadata (is_active = true) but haven't touched the platform in months. 

Check `nexus-analyst-demo.acme.dim_users.last_login_date` too. It's updated daily. 

**sarah.chen** — 11:28 AM
Thanks Rajiv. Using `last_login_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)`. 

---

# #data-help — 2026-02-02

**marcus.hopkins** — 2:14 PM
@dan.lee is the `fact_workflow_runs` table missing data for the Amsterdam (EMEA) region today? I'm seeing a massive dip in `step_count` for all Dutch customers starting at 08:00 UTC. 

**dan.lee** — 2:20 PM
Let me look at the ingestion logs... 
Wait, I see a spike in `error_code = 'ERR-999'` in `fact_workflow_runs` for that window. 

**dan.lee** — 2:25 PM
Found it. The webhook listener in the AMS-01 data center had a memory leak during the v2.4.1 deploy. Eng rolled it back at 09:30 UTC. 

The data isn't missing, it's just failed runs. If you look at `status`, they'll all be 'failed'. 

**marcus.hopkins** — 2:27 PM
Okay, so it’s not a data pipeline issue, it’s a product outage. I’ll let the CS team know why their dashboards are red. 

**dan.lee** — 2:30 PM
Yep. "Systemic failure" not "Data failure". My favorite kind of distinction. 

---

# #data-help — 2026-02-04

**rajiv.menon** — 10:00 AM
Morning all. Reminder that we are doing the BigQuery schema migration for the `dim_plans` table tonight. We’re adding `storage_gb` and `sla_uptime_pct` columns to the FLAT view. 

No downtime expected, but if your scheduled Looker tiles break tomorrow morning, check your `SELECT *` statements. 

**sarah.chen** — 10:05 AM
Are we finally adding the `workflow_run_quota_per_month` to that table too? I'm tired of hardcoding `10000` for Pro users in my SQL. 

**rajiv.menon** — 10:06 AM
Yes, it's in there now. 
`nexus-analyst-demo.acme.dim_plans` will be the source of truth for quotas moving forward. 

**dan.lee** — 10:10 AM
@sarah.chen FYI—Business tier quota is 100k, not unlimited. Only Enterprise is `NULL` (unlimited). Make sure your CASE statements handle the NULLs correctly or you’ll get some weird math on "Percent of Quota Used" metrics.

**sarah.chen** — 10:12 AM
`COALESCE(workflow_run_quota_per_month, 999999999)` it is. Thanks Dan. 

**marcus.hopkins** — 10:15 AM
Donuts in the Amsterdam office if anyone is visiting! 🍩 (I know, I'm the only one here today, more for me).

---

# #data-help — 2026-02-12

**sarah.chen** — 9:15 AM
Hey @dan.lee — I’m trying to pull the NRR (Net Revenue Retention) for the MM (Mid-Market) segment for Q1 so far, but my numbers are looking... insane? I'm getting 215% for `Global Logistics Corp`. I know they expanded, but they didn't triple their spend. 

**dan.lee** — 9:22 AM
Are you joining `dim_customers` to `fact_subscriptions`? 

**sarah.chen** — 9:24 AM
Yeah. `SELECT company_name, sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions JOIN ...` 

**dan.lee** — 9:26 AM
That’s the issue. `fact_subscriptions` is a ledger of every change. If a customer upgraded three times in the last month, you're summing all those rows together. You need to filter for `is_current = TRUE` if you want a point-in-time snapshot, OR use a date window on `start_date` and `end_date`. 

**sarah.chen** — 9:28 AM
Ugh, right. I forgot `fact_subscriptions` is type-2-ish. Is there a view that handles the month-over-month delta for me? 

**rajiv.menon** — 9:30 AM
@sarah.chen check `nexus-analyst-demo.acme.fact_mrr_movements` (it's not in the FLAT root yet, it’s in the `restricted` schema for Finance, but you have access). It breaks out `new_business`, `expansion`, `contraction`, and `churn` per customer per month. 

**sarah.chen** — 9:35 AM
Found it. This is much better. Wait, why is `Logitech-SaaS-Partner-6` showing a $0 expansion even though they added 50 seats?

**dan.lee** — 9:40 AM
Probably because they are on a "Legacy Business" tier that we deprecated in 2024. The pricing logic in the `mrr_movements` script sometimes trips on those if the `plan_tier` doesn't match the `dim_plans` table exactly. I’ll add it to my backlog.

---

# #random — 2026-02-13

**marcus.hopkins** — 11:45 AM
Does anyone know if the food truck on 4th Street (the taco one) is still there on Fridays? 🌮

**rajiv.menon** — 11:47 AM
They moved one block over because of the construction near the Salesforce tower. Still the best carnitas in SF.

**marcus.hopkins** — 11:50 AM
Crying in Amsterdam. We have... pickled herring. 🐟

---

# #data-help — 2026-02-15

**chloe.vargas** — 2:00 PM
@data-team I'm building a "Health Score" dashboard for the CSMs. I need a definitive "Last Active Date" for a customer. 

Should I use `last_login_date` from `dim_users` or should I look at `fact_workflow_runs` to see when they last actually *did* something? 

**dan.lee** — 2:05 PM
Great question. `last_login_date` is just "who looked at the UI." A lot of our biggest Enterprise customers (like `Omega Manufacturing`) have workflows that run 24/7 via API, but their admins haven't logged in for weeks. 

I’d recommend a max of both. Look at `triggered_at` in `nexus-analyst-demo.acme.fact_workflow_runs`. 

**sarah.chen** — 2:08 PM
Careful with `fact_workflow_runs` though—it's 400M rows. If you're doing a `MAX()` on that table without a partition filter on `triggered_at`, BigQuery is going to eat our budget for lunch. 

**chloe.vargas** — 2:10 PM
Okay, good tip. How do I filter it efficiently? 

**rajiv.menon** — 2:12 PM
Always include `WHERE triggered_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)` in your subquery. Most CSMs only care if they've been active in the last month anyway. 

**chloe.vargas** — 2:15 PM
What about the `step_count`? If a workflow runs but has 0 steps, does that count as engagement? 

**dan.lee** — 2:17 PM
No, 0 steps usually means a failed trigger or an empty conditional. I'd filter for `step_count > 0`. 

---

# #data-help — 2026-02-18

**jordan.smith** — 9:00 AM
Question on the `fact_invoices` table. I see some records for `Acme Internal` accounts. Are these being filtered out of the ARR metrics? 

**rajiv.menon** — 9:05 AM
They should be. The standard `current_mrr_usd` in `dim_customers` excludes any `customer_id` where `industry = 'Internal'`. 

**jordan.smith** — 9:10 AM
Okay, because the Board Deck prep is showing $39.2M ARR, but my query on `fact_subscriptions` is showing $39.5M. The $300k difference matches the "test" accounts we set up for the Sales Engineering team. 

**sarah.chen** — 9:12 AM
@jordan.smith Are you using the `FLAT` view? I updated the `dim_customers` logic yesterday to flag those SE accounts as `status = 'internal'`. Use that in your `WHERE` clause. 

**jordan.smith** — 9:15 AM
Got it. `nexus-analyst-demo.acme.dim_customers` where `status = 'active'` it is. 

---

# #data-help — 2026-02-20

**dan.lee** — 4:30 PM
🚨 **HEADS UP** 🚨
We are seeing a high volume of `error_code = 'RATE_LIMIT_EXCEEDED'` for several Business tier customers in `fact_workflow_runs` this afternoon. 

It looks like `Skyline Systems` and `TechFlow Partners` are hitting the 100k monthly run quota early. 

**marcus.hopkins** — 4:35 PM
@chloe.vargas — `Skyline Systems` is your account, right? They might need an emergency Enterprise upgrade if they're capped out on day 20 of the month. 

**chloe.vargas** — 4:40 PM
On it. I’ll check their usage in the dashboard. Can someone confirm the exact count for them? 

**dan.lee** — 4:42 PM
```sql
SELECT 
  count(*) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-772' -- Skyline
  AND triggered_at >= '2026-02-01'
  AND status = 'success'
```
They are at 104,202 runs. The system hasn't hard-blocked them yet because of the 10% grace buffer, but they'll hit the hard ceiling at 110k. 

**chloe.vargas** — 4:45 PM
Thanks Dan. Calling their VP Ops now. This is a great expansion trigger. 💸

---

# #general — 2026-02-21

**rajiv.menon** — 10:00 AM
Standup is moved to 10:30 AM today. The coffee machine on the 3rd floor is leaking and the whole kitchen is a lake. 🛶

**sarah.chen** — 10:02 AM
Is the data warehouse still dry? 

**rajiv.menon** — 10:03 AM
Cloud-native, Sarah. The rain can't hurt us in GCP. ☁️

---

# #data-help — 2026-02-24

**marcus.hopkins** — 3:15 PM
Quick one — in `dim_users`, what’s the difference between `is_active` and the user being "provisioned"? 

**dan.lee** — 3:20 PM
`is_active = TRUE` means they haven't been deleted or suspended. A user could be "active" but not have logged in for 6 months. 

If you want "Active Users" for the VRS (Volume, Runs, Steps) report, you need to join to `fact_user_events` and look for `event_type = 'login'` or `event_type = 'workflow_created'` in the last 28 days. 

**marcus.hopkins** — 3:22 PM
Cool. Working on the MAU (Monthly Active Users) vs. Licensed Seats ratio. Business tier customers are paying for 50 seats but some only use 10. Product wants to nudge them to invite more teammates. 

**sarah.chen** — 3:25 PM
Check `seat_count_licensed` in `dim_customers`. For the Business tier, that’s almost always `50` (our minimum). If they have 10 MAUs, their "Seat Utilization" is 20%. 

**marcus.hopkins** — 3:27 PM
Perfect. `nexus-analyst-demo.acme.dim_customers` has everything I need then. Cheers.

---

# #random — 2026-02-25

**rajiv.menon** — 11:45 AM
Anyone leaving for lunch? I’m hitting that new taco spot on Mission. 🌮

**dan.lee** — 11:46 AM
In a meeting with the Amsterdam team. They’re already at the pub probably. 🍻

**marcus.hopkins** — 11:48 AM
I’m in. Give me 5 mins to finish this query for the Q1 board deck. If I see one more `null` value in `industry` for an Enterprise account I’m going to lose it.

**rajiv.menon** — 11:50 AM
Blame the AEs. They never fill out the CRM fields properly. 

---

# #data-help — 2026-02-26

**elara.vance** — 9:12 AM
Hey data folks — I’m trying to calculate Net Revenue Retention (NRR) for the Mid-Market (MM) segment last month. My number looks way too high (like 140%). 

**sarah.chen** — 9:15 AM
@elara.vance are you looking at `fact_subscriptions`? And are you filtering for `is_current`? 

**elara.vance** — 9:17 AM
Yeah, using this:
```sql
SELECT 
  sum(mrr_usd) 
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE start_date <= '2026-01-31' 
  AND (end_date > '2026-01-31' OR end_date IS NULL)
```

**dan.lee** — 9:20 AM
That’s the issue. `fact_subscriptions` is a log of every change. If a customer upgraded twice in January, you’re double-counting their MRR because you aren't filtering out the old rows for that period. 

For NRR, you need to compare the cohort’s MRR at the start of the month vs the end of the month. Use the `change_type` column to see who was an `upgrade` vs `downgrade`.

**sarah.chen** — 9:22 AM
Also, Elara, make sure you aren't accidentally including New Logo bookings in your NRR. NRR should only be `Expansion + Resurrected - Churn - Contraction` over the `Starting Base`. 

If you include New Logos, you're looking at Gross Retention or just simple MRR growth. 

**elara.vance** — 9:25 AM
Got it. Does `dim_customers.account_tier` map correctly to the subscription records?

**dan.lee** — 9:26 AM
Mostly, but remember that `account_tier` in `dim_customers` is their *current* status. If you’re doing historical reporting (like what were they in 2025?), you have to be careful. But for Jan 2026 it should be fine. 

---

# #data-help — 2026-03-02

**marcus.hopkins** — 2:05 PM
Quick question on VRS (Volume, Runs, Steps). I see `step_count` in `fact_workflow_runs`. Is a "step" billed differently than a "run"? 

**sarah.chen** — 2:10 PM
No, we only bill on `runs` (the triggers). The `step_count` is a proxy for platform load/intensity. We use it for the "Infrastructure Cost per Customer" model that Finance is obsessed with. 

If a workflow has 50 steps but only runs once, it's 1 run. If it has 2 steps but runs 10,000 times, that’s what hits the customer’s quota. 

**marcus.hopkins** — 2:12 PM
Ah, okay. So for the "Power User" dashboard, I should probably look at people with high `step_count` per run? That indicates more complex automation.

**dan.lee** — 2:15 PM
Exactly. A "Heavy" user usually has `step_count > 10` on average. 

**marcus.hopkins** — 2:16 PM
```sql
SELECT 
  customer_id, 
  avg(step_count) as avg_complexity
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
```
Whoa, 'CUST-441' (Velocity Tech) has an average step count of 82. What are they building over there? 

**sarah.chen** — 2:18 PM
They’re a Business tier account. They basically rebuilt their entire ERP inside our platform. Let’s not break their workflows or the CSM will have a heart attack. 

---

# #general — 2026-03-05

**rajiv.menon** — 8:30 AM
Reminder: The Amsterdam office is closed today for a local holiday. Expect delays on any tickets assigned to the EMEA support or engineering squads. 🇳🇱

**dan.lee** — 8:32 AM
Explains why my PR has been sitting there for 4 hours. 

---

# #data-help — 2026-03-10

**chloe.vargas** — 11:00 AM
Trying to pull a list of all Enterprise accounts that are "At Risk" based on login activity. Is `last_login_date` in `dim_users` updated in real-time? 

**dan.lee** — 11:05 AM
Refreshes every 2 hours via the dbt sync. 

**chloe.vargas** — 11:06 AM
Perfect. I'm seeing a few accounts where `last_login_date` for ALL users is > 14 days ago. 

**sarah.chen** — 11:10 AM
@chloe.vargas make sure you filter for `is_active = TRUE` in `dim_users`. Sometimes customers leave old provisioned seats for people who left the company, and those shouldn't count against their engagement score. 

**chloe.vargas** — 11:12 AM
Good point. Does this look right for finding the ghost towns?
```sql
SELECT 
  c.company_name, 
  max(u.last_login_date) as last_seen
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Enterprise'
  AND u.is_active = TRUE
GROUP BY 1
HAVING max(u.last_login_date) < DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
```

**dan.lee** — 11:15 AM
Logic holds up. Run it. 

**chloe.vargas** — 11:20 AM
Ouch. "Global Logistics Corp" (CUST-902) hasn't had a login in 3 weeks. They pay us $120k ARR. Calling the AE now. 🚩

---

# #random — 2026-03-12

**marcus.hopkins** — 4:20 PM
Is the snack bar out of the dried mango again? This is a Tier 1 incident. 🥭

**rajiv.menon** — 4:22 PM
Checking the `fact_pantry_usage` table now... looks like someone (Dan?) did a bulk export of the mangoes at 9 AM. 

**dan.lee** — 4:25 PM
I regret nothing. They're fuel for the BigQuery migration. 

---

# #data-help — 2026-03-15

**sarah.chen** — 9:00 AM
Heads up for everyone using the flat files: I’ve added `acquisition_channel` to `dim_customers`. 

Marketing wants to see if customers from `organic_search` have better 6-month retention than `paid_social`. 

**marcus.hopkins** — 9:15 AM
Nice. I’ll update the LTV (Lifetime Value) models. 

Does `acquisition_channel` track the first touch or the last touch before signup? 

**sarah.chen** — 9:20 AM
It’s First Touch. If they clicked a LinkedIn ad in 2024 but didn't sign up until 2025 after a Google search, they’re still marked as `paid_social` based on the initial lead capture. 

**dan.lee** — 9:22 AM
The attribution logic is in the `stg_web_events` model if you want to dig into the mess, but `dim_customers` is the source of truth for the board. Stick to the flat table.

#data-help — 2026-03-20

**marcus.hopkins** — 10:45 AM
Quick sanity check on NRR (Net Revenue Retention). I’m pulling from `nexus-analyst-demo.acme.fact_subscriptions` and my denominator for the Cohort (March 2025) is looking way too high. 

**sarah.chen** — 10:48 AM
Are you filtering for `is_current`? 

**marcus.hopkins** — 10:50 AM
Yeah, but I’m trying to see the delta. If a customer was at $1k MRR in March 2025 and they are at $1.5k now, that $500 expansion should be in the numerator, right?

**rajiv.menon** — 10:52 AM
Marcus, don't forget that NRR needs to exclude New Logos from the current month. If you just sum `mrr_usd` for `start_date` in March 2026, you're getting Gross Retention + Expansion + New Biz. 

You need to join `fact_subscriptions` to itself on `customer_id` where the `start_date` of the base sub is < the beginning of the period. 

**dan.lee** — 10:55 AM
Just use the `change_type` column. That’s why we built it. 
`SELECT sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE change_type = 'RENEWAL' OR change_type = 'UPGRADE'`
If you see `NEW_BIZ`, drop it from the NRR numerator. 

**marcus.hopkins** — 11:02 AM
Found the bug. I was including "CloudSync" (CUST-405) in the denominator but they were actually `status = 'PAUSED'` in `dim_customers` during that window. Fixed. 

---

# #random — 2026-03-22

**chloe.vargas** — 8:15 AM
Who left the avocado toast in the toaster oven in the SF kitchen? It’s currently a charcoal brick and the 4th floor smells like a campfire. 🔥

**rajiv.menon** — 8:20 AM
Not me, I’m in the Amsterdam office today. Though the espresso machine here is making a high-pitched screaming sound. Might be sentient. 

**dan.lee** — 8:22 AM
The SF toaster oven is now a `fact_kitchen_disaster`. Please refrain from manual overrides on the heat settings. 

---

# #data-help — 2026-03-25

**sarah.chen** — 2:10 PM
Does anyone know why `fact_workflow_runs` has a bunch of rows with `status = 'ERROR'` but `error_code` is NULL? 

Looking specifically at "DataFlow Systems" (CUST-112). They had 14k runs yesterday and 2k failed with no code. 

**dan.lee** — 2:15 PM
That usually means the worker node was killed before the error handler could write back to the DB. Usually a memory limit issue on the customer's side. 

Check `duration_ms` in `nexus-analyst-demo.acme.fact_workflow_runs`. If it's exactly 300,000ms, it’s a timeout. 

**sarah.chen** — 2:18 PM
Yep, exactly 300k. They’re trying to process huge CSVs on the Pro plan. I'll flag this for their CSM. They need to move to Business tier for the higher memory limit. 💰

---

# #ops-announcements — 2026-03-28

**rajiv.menon** — 9:00 AM
VRS (Volume Reporting System) is lagging. If you are looking at `fact_user_events` for anything that happened in the last 4 hours, it might be incomplete. 

**marcus.hopkins** — 9:05 AM
Does this affect the `last_login_date` in `dim_users`? 

**rajiv.menon** — 9:10 AM
Yes. The nightly dbt job will clean it up, but the intra-day "flat" tables are going to be stale until the Kinesis stream catches up. 

---

# #data-help — 2026-04-02

**chloe.vargas** — 11:30 AM
I’m seeing a discrepancy in seat counts. 
`dim_customers.seat_count_licensed` for "OmniCorp" (CUST-771) says 500. 
But if I count unique `user_id` in `dim_users` for that `customer_id`, I get 512. 

How can they have 12 more users than licenses? 

**dan.lee** — 11:35 AM
Check `is_active` in `dim_users`. 

**chloe.vargas** — 11:37 AM
Even with `is_active = TRUE`, it’s 508. 

**dan.lee** — 11:40 AM
Standard over-provisioning. The Business plan allows a 10% buffer before we trigger an automated true-up invoice. 

If you want the "billable" number, always use `seat_count` from `nexus-analyst-demo.acme.fact_subscriptions` where `is_current = TRUE`. 

The `dim_users` table just shows who has an account, but `fact_subscriptions` is what Finance actually hits them for. 

**chloe.vargas** — 11:42 AM
Got it. I'll stop using the user count for revenue projections. 🤦‍♀️

---

# #random — 2026-04-05

**rajiv.menon** — 12:00 PM
Is it just me or is the "Dark Mode" on the new dashboard more of a "Slightly Darker Grey Mode"? 

**sarah.chen** — 12:05 PM
It’s #121212. Any darker and the contrast ratio for the error codes (Red) fails accessibility. 

**marcus.hopkins** — 12:10 PM
I just want a mode that hides the churn charts on Fridays so I can enjoy my weekend. 📉🚫

**dan.lee** — 12:12 PM
`SELECT * FROM reality WHERE mood = 'HAPPY'` returns 0 rows, Marcus. 

---

# #data-help — 2026-04-10

**sarah.chen** — 3:45 PM
Heads up—Marketing just changed the UTM parameters for the Q2 "Automate Everything" campaign. 

If you see `acquisition_channel` coming in as `unknown` in `dim_customers` for new signups today, it's because the `stg_web_events` logic hasn't been updated to map `src=social_influence` to `paid_social`. 

**marcus.hopkins** — 3:50 PM
Again? That’s the third time this quarter. 

**sarah.chen** — 3:52 PM
I’m PRing a fix now. If you're running LTV reports for April, wait until tomorrow's refresh. 

**dan.lee** — 3:55 PM
Make sure you update the mapping in the BigQuery FLAT view too, not just the dbt model. I don't want the execs seeing "Unknown" on the Monday morning call. `nexus-analyst-demo.acme.dim_customers` needs to be clean.

# #random — 2026-04-11

**marcus.hopkins** — 9:15 AM
Is the SF office espresso machine down again? It’s making a sound like a server rack dying. ☕️💀

**rajiv.menon** — 9:20 AM
Yeah, the pump is shot. I’m currently walking to Blue Bottle. Taking orders? 

**chloe.vargas** — 9:21 AM
Oat milk latte, please. I’ll Venmo you. Also, can we talk about why the 10th floor smells like burnt popcorn? 

**dan.lee** — 9:25 AM
That’s probably the engineering team celebrating the VRS (Virtual Runtime System) v3 deployment. Or something actually caught fire. Hard to tell with those guys. 

---

# #data-help — 2026-04-12

**marcus.hopkins** — 10:30 AM
Hey @dan.lee — I’m trying to calculate Net Revenue Retention (NRR) for the Q1 Board Deck. When I join `fact_subscriptions` to itself to get MoM delta, I’m getting 142%. That feels… way too high. Even for us. 

**dan.lee** — 10:35 AM
Check your join key on `change_type`. If you're just summing `mrr_usd` by `customer_id` across months, you might be double-counting customers who upgraded mid-cycle and have two "is_current" records in the same snapshot period if you aren't filtering for the specific `month_end`. 

**marcus.hopkins** — 10:38 AM
Wait, how can a customer have two `is_current = TRUE` rows? 

**sarah.chen** — 10:40 AM
They can't in the final `dim_customers`, but in `fact_subscriptions`, if they upgraded from Pro to Business on the 15th, and you're grouping by `month`, you'll see both records unless you filter for `status = 'active'` and the max `start_date` for that period. 

Use the `nexus-analyst-demo.acme.fact_subscriptions` table and filter for `is_current = TRUE` specifically. Also, watch out for the `currency_code` (though we’re 99% USD now, some old EMEA legacy stuff still pops up as EUR in the raw logs). 

**marcus.hopkins** — 10:45 AM
Ah, found it. I was missing the `billing_cycle` exclusion. The Enterprise deals with multi-year offsets were messing up the denominator. 📉

---

# #data-help — 2026-04-15

**chloe.vargas** — 2:15 PM
Does anyone know why `seat_count_licensed` for "Cyberdyne Systems" is showing 0 in `dim_customers`? They’re a Business tier customer. 

**dan.lee** — 2:20 PM
Let me look... `SELECT status FROM nexus-analyst-demo.acme.dim_customers WHERE company_name = 'Cyberdyne Systems'`. 

They’re marked as `status = 'paused'`. CS put them on a holding plan while they sort out their internal procurement. On a paused plan, `seat_count` in the subscription table goes to 0 so we don't trigger the automated seat overage alerts. 

**chloe.vargas** — 2:22 PM
Shouldn't they be excluded from the "Active Customer" count then? 

**dan.lee** — 2:25 PM
Yes. If you’re doing the official KPI report, always filter for `status = 'active'`. Paused and Churned should be ignored for ARR. 

---

# #random — 2026-04-18

**sarah.chen** — 11:00 AM
Reminder: The "Data-is-Dope" lunch is moved to the courtyard because the ventilation in Room 402 is still broken. 🥗

**rajiv.menon** — 11:05 AM
Will there be tacos? 🌮

**sarah.chen** — 11:06 AM
Only if you can prove you didn't use `SELECT *` on the production database this week, Rajiv. 

**rajiv.menon** — 11:10 AM
Guess I’m buying my own lunch. 

---

# #data-help — 2026-04-20

**marcus.hopkins** — 4:00 PM
I’m looking at `fact_workflow_runs` to see if there's a correlation between `duration_ms` and churn risk. 

I’m seeing a massive spike in errors (`error_code = 'ERR_TIMEOUT'`) for customers in the `region = 'EMEA'` between April 12th and April 14th. Did we have an outage? 

**sarah.chen** — 4:05 PM
That was the VRS v3 rollout. The Frankfurt cluster had a configuration mismatch on the webhook timeout limit. It was resolved in the 2026-04-14 22:00 UTC patch. 

**marcus.hopkins** — 4:08 PM
Okay, so I should probably exclude those dates from the "Platform Health" metrics? 

**dan.lee** — 4:10 PM
Keep them in the raw data, but tag them as "Known Issue" in your viz. The execs need to see the impact of the downtime on the SLA credits we’re going to have to issue next month. 

Check `nexus-analyst-demo.acme.fact_invoices` for any "Credit Note" types appearing next week. That'll be Finance cleaning up the mess. 

---

# #data-help — 2026-04-22

**rajiv.menon** — 9:30 AM
Quick question—what is the engagement threshold for "Power User"? Is it just login frequency? 

**sarah.chen** — 9:35 AM
We usually define it as > 50 successful `workflow_runs` in a 7-day period. 

`SELECT user_id FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'SUCCESS' GROUP BY 1 HAVING COUNT(*) > 50`

If you use `last_login_date` from `dim_users`, you'll get people who just hover but don't actually automate anything. We want the builders. 

**rajiv.menon** — 9:40 AM
Perfect. Trying to find targets for the new "Advanced Logic" webinar. 

---

# #data-help — 2026-04-25

**chloe.vargas** — 1:15 PM
Is `mrr_usd` in `fact_subscriptions` annualized already or is it monthly? 

**dan.lee** — 1:20 PM
It’s Monthly Recurring Revenue. If you want ARR, you multiply by 12. 

**chloe.vargas** — 1:22 PM
Even for the Enterprise plans that pay annually upfront? 

**dan.lee** — 1:25 PM
Yes. The table normalizes it to monthly so we can compare SMB (monthly billing) and Enterprise (annual billing) on the same timeline. 

`billing_cycle` tells you how they pay, but `mrr_usd` is always the 1-month equivalent. 

**chloe.vargas** — 1:27 PM
Found a bug then. "OmniCorp" has an ACV of $120k, but their `mrr_usd` is showing as $120k in the table. 🤦‍♂️

**dan.lee** — 1:30 PM
Ugh, Sales Ops must have entered the total contract value into the MRR field in the CRM again. Let me go yell at the Salesforce sync. Don't use that number for the forecast yet. 

**sarah.chen** — 1:32 PM
I’ll add a data quality check to the dbt model for `mrr_usd > 50000` just in case. No one's MRR should be that high unless it’s a massive Enterprise deal we’d all know about.

---

# #random — 2026-04-26

**marcus.thorne** — 11:15 AM
Is the espresso machine in the SF lounge still leaking? I tried to pull a double shot and ended up with a small lake on my shoes. 

**elena.rossi** — 11:18 AM
Yeah, Office Ops said the part is backordered. Use the one in the 4th-floor pantry, it’s the fancy new Jura. 

**marcus.thorne** — 11:20 AM
Bless you. Walking up two flights of stairs is my cardio for the day anyway.

---

# #data-help — 2026-04-27

**elena.rossi** — 2:45 PM
Hey @sarah.chen — I’m trying to calculate Net Revenue Retention (NRR) for the MM (Mid-Market) segment for Q1, but my numbers are coming out to like 190%. That can’t be right. We’re good, but we’re not *that* good. 

**sarah.chen** — 2:50 PM
Are you joining `fact_subscriptions` to itself using `changed_from_subscription_id`? 

**elena.rossi** — 2:52 PM
I was just summing `mrr_usd` where `is_current = true` and comparing it to the sum from Jan 1st. 

**sarah.chen** — 2:55 PM
That’s the problem. You’re catching all the new logos from Q1 in your "current" bucket. To get true NRR, you have to look at the cohort that existed on Jan 1 and see their *evolution*. 

Try this: 
`SELECT SUM(curr.mrr_usd) / SUM(prev.mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions curr JOIN nexus-analyst-demo.acme.fact_subscriptions prev ON curr.changed_from_subscription_id = prev.subscription_id WHERE prev.start_date < '2026-01-01' AND curr.change_type IN ('UPGRADE', 'RENEWAL', 'DOWNGRADE')`

Also, make sure you filter for `account_tier = 'MM'` in `dim_customers`. 

**elena.rossi** — 3:10 PM
Ah, the `change_type` filter is what I missed. I was accidentally counting `NEW_SUBSCRIPTION` as expansion. Fixed it, now I'm seeing 112%. Much more realistic. Thanks!

---

# #data-help — 2026-04-29

**rajiv.menon** — 10:05 AM
Does anyone know why the `fact_workflow_runs` table has a massive spike in `error_code = 'VRS_503'` for yesterday afternoon? 

**dan.lee** — 10:10 AM
That was the "Virtual Runtime Service" glitch. The Amsterdam cluster hit a memory limit because someone (won't name names, but it rhymes with Big-Retail-Co) tried to trigger 1M webhooks simultaneously. 

**rajiv.menon** — 10:12 AM
Got it. Is it safe to exclude those from the "Success Rate" KPI for the board deck? 

**sarah.chen** — 10:15 AM
Technically it was downtime, so no. We have to report it. But you can add a footnote about the "VRS 503" surge. Check `nexus-analyst-demo.acme.fact_workflow_runs` and you’ll see the `duration_ms` is also nearly 0 for those since they failed instantly at the gateway.

---

# #ops-standup — 2026-05-01

**chloe.vargas** — 9:00 AM
Reminder: Monthly close starts today. Please don't push any major changes to the `fact_invoices` logic in dbt until Finance signs off on the April numbers. 

**dan.lee** — 9:05 AM
Copy that. I'm just running a one-off script to tag the "Credit Note" entries from the outage. It shouldn't touch the core model. 

---

# #data-help — 2026-05-02

**marcus.thorne** — 4:20 PM
Quick check on `dim_plans`—the `workflow_run_quota_per_month` for the Business tier is 100k, right? I see a customer "Skyline Systems" that has done 150k runs this month but they haven't been throttled. 

**sarah.chen** — 4:25 PM
Business tier has a "soft" cap. We don't hard-kill their workflows until they hit 20% overage, then CS gets an automated alert to ping them for an Enterprise upgrade. 

If you want to see who's currently over their quota, run this:

`SELECT c.company_name, COUNT(r.run_id) as total_runs, p.workflow_run_quota_per_month FROM nexus-analyst-demo.acme.fact_workflow_runs r JOIN nexus-analyst-demo.acme.dim_customers c ON r.customer_id = c.customer_id JOIN nexus-analyst-demo.acme.dim_plans p ON c.current_plan_tier = p.plan_tier WHERE r.triggered_at >= '2026-04-01' GROUP BY 1, 3 HAVING COUNT(r.run_id) > p.workflow_run_quota_per_month`

**marcus.thorne** — 4:30 PM
Super helpful. "Skyline" is definitely a candidate for the Enterprise move. Their ACV is only $18k right now (Business plan, ~10 seats). They’re getting a steal on those runs.

**dan.lee** — 4:32 PM
Check their `acquisition_channel` in `dim_customers` too. If they came in through the "Referral" program, they might have a temporary quota bump. 

---

# #data-help — 2026-05-04

**elena.rossi** — 11:45 AM
Quick sanity check: `nexus-analyst-demo.acme.dim_users` — `last_login_date` is in UTC, correct?

**dan.lee** — 11:47 AM
Everything in the warehouse is UTC. If you're building a dashboard for the Amsterdam team, you'll need to `DATETIME_ADD` or use `DATE_DIFF` carefully. 

**elena.rossi** — 11:50 AM
Ugh, I hate timezones. My "Daily Active Users" chart looks weird because the West Coast logins on Monday night are showing up as Tuesday morning in the raw data. 

**sarah.chen** — 11:55 AM
Use `TIMESTAMP(last_login_date, "America/Los_Angeles")` if you're reporting to the SF execs. It makes the "Active Users" dip on Sundays look less scary. 

---

# #random — 2026-05-04

**rajiv.menon** — 12:15 PM
Is it just me or is the warehouse lagging more than the usual 2 hours today? 

**dan.lee** — 12:18 PM
Fivetran is having a bad day. There was a schema change in the production `events` table that tripped up the sync. It's catching up now, but expect about a 4-hour delay until the 2 PM refresh. 

**rajiv.menon** — 12:20 PM
Cool, I'll go get another coffee from the 4th floor. Marcus wasn't kidding, that Jura machine is life-changing.

---

# #data-help — 2026-05-05

**elena.rossi** — 9:15 AM
Does anyone have a clean snippet for Gross Revenue Retention (GRR) by `account_tier`? I'm trying to compare SMB vs Enterprise for the Board deck and my numbers for April look... inflated. 

**dan.lee** — 9:22 AM
@elena.rossi You’re probably double-counting the `change_type = 'upgrade'` events in `fact_subscriptions`. For GRR, you only want to look at the starting MRR and subtract the `downgrade` and `churn` amounts. Don't include the expansion. 

Try this:
`SELECT c.account_tier, SUM(s.mrr_usd) as beginning_mrr FROM nexus-analyst-demo.acme.fact_subscriptions s JOIN nexus-analyst-demo.acme.dim_customers c ON s.customer_id = c.customer_id WHERE s.start_date = '2026-04-01' AND s.is_current = true GROUP BY 1`

Wait, that's not right either because `is_current` only shows today. You need to snapshot it. Use the `month_end` logic we built in the `fct_mrr_movements` mart (or just query the raw `fact_subscriptions` with a date filter on `start_date`).

**elena.rossi** — 9:30 AM
Thanks Dan. I think I see the issue. I was joining `dim_customers.current_mrr_usd` which is a "now" value, not a "then" value. I’ll stick to `fact_subscriptions`. 

**marcus.thorne** — 10:05 AM
Speaking of Enterprise — did the "Vertex Corp" deal close in the warehouse yet? I see it in Salesforce as "Closed/Won" but `dim_customers` still has them as `current_plan_tier = 'Business'`.

**dan.lee** — 10:10 AM
Checked the logs. The sync from SFDC to the warehouse runs at midnight. If it closed this morning, you won't see it until the 2 AM refresh tomorrow. If you need it for a report *right now*, you'll have to manually override the CSV or just wait. 

**marcus.thorne** — 10:12 AM
I'll wait. But heads up, they're 300 seats. That should jump the Enterprise ARR significantly. 

---

# #random — 2026-05-05

**rajiv.menon** — 12:45 PM
Who’s up for the taco truck today? The one on 3rd is back. 

**sarah.chen** — 12:46 PM
Me! But only if we don't talk about the `user_id` vs `email_domain` join issues I've been having all morning. 

**rajiv.menon** — 12:48 PM
Deal. No data talk. Just carnitas. 

**elena.rossi** — 12:50 PM
Can you grab me a burrito? I’m stuck in NRR-hell. No onions. 

---

# #data-help — 2026-05-05

**sarah.chen** — 2:15 PM
Quick question on `fact_user_events`. I'm seeing a lot of `event_type = 'workflow_created'` but the `triggered_at` in `fact_workflow_runs` for those same users is empty. Is it possible to create a workflow and never run it?

**dan.lee** — 2:18 PM
Absolutely. About 40% of our Free tier users do that. They set up the integration, get scared by the "Auth" screen or the mapping, and just leave it sitting there. 

If you want to find "Active Engaged" customers, you should filter by:
`SELECT DISTINCT customer_id FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'success' AND triggered_at >= CURRENT_DATE() - 7`

That’s the "Aha!" moment we track — the first successful run.

**sarah.chen** — 2:22 PM
Got it. I'm trying to build a cohort for "CloudScale" (they’re on the Pro plan). They’ve added 50 users this month but their workflow run count is flat. Feels like a churn risk. 

**marcus.thorne** — 2:25 PM
"CloudScale" is a referral from the Amsterdam office. I think they’re still in the "onboarding" phase. Their CSM is looking at their seat utilization, which is high, but yeah, the actual automation value isn't there yet. 

---

# #ops-announcements — 2026-05-06

**dan.lee** — 9:00 AM
**REMINDER:** We are deprecating the old `acme_raw` datasets by the end of the month. Please update all your Looker dashboards and Hex notebooks to point to the FLAT schema in `nexus-analyst-demo.acme`. 

If your query starts with `FROM acme_prod.customers`, it WILL BREAK. 

Use the new canonical dims:
- `dim_customers`
- `dim_users`
- `fact_subscriptions`

If you find a column missing in the flat tables that was in the old ones, let me know. 

**rajiv.menon** — 9:15 AM
Does this affect the "Weekly Marketing Spend" sheet? 

**dan.lee** — 9:17 AM
Yes, Rajiv. Anything pulling from the warehouse. I’ll help you migrate the `acquisition_channel` logic later today. 

---

# #data-help — 2026-05-06

**elena.rossi** — 11:00 AM
Okay, I'm looking at NRR again. If a customer like "Global Dynamics" moves from 50 seats to 75 seats mid-month, `fact_subscriptions` shows two rows for that month, right? 

**dan.lee** — 11:05 AM
Exactly. The first row will have `is_current = false` and an `end_date` that matches the `start_date` of the second row. The `change_type` on the second row should be `'expansion'`. 

If you want to annualize the bookings for Marcus's team, you need to be careful. A mid-month add only reflects the pro-rated MRR for that specific month in the invoice, but the `mrr_usd` column in `fact_subscriptions` is always the *full* monthly value. 

`SELECT customer_id, (mrr_usd * 12) as arr FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = true`

That will give you the current run-rate ARR. 

**elena.rossi** — 11:10 AM
Perfect. That explains why my sum of `fact_invoices.amount_usd` was lower than my ARR/12 calculation. Pro-rating is a nightmare. 

**dan.lee** — 11:12 AM
Welcome to B2B SaaS. It only gets worse when they pay annually and we have to do revenue recognition. Don't even look at the `period_start` columns yet if you value your sanity.

---

# #random — 2026-05-07

**sarah.jenkins** — 8:45 AM
Is the espresso machine on the 3rd floor leaking again or is it just me? There’s a puddle the size of Lake Tahoe under the descale light. 

**marcus.wu** — 8:52 AM
It’s definitely leaking. Facilities said they’re waiting on a part for the steam wand. Use the one in the 4th floor micro-kitchen for now, but watch out for the EMEA sales team, they’re taking over the big table for their offsite.

**rajiv.menon** — 10:15 AM
Lunch poll: Super Duper or the Poke place? 
- 🍔 Super Duper (4)
- 🐟 Poke (2)

---

# #data-help — 2026-05-07

**elena.rossi** — 1:30 PM
Hey @dan.lee — I’m trying to calculate Gross Retention for the Board deck. I’m joining `dim_customers` to `fact_subscriptions` to get the MRR from 12 months ago vs today. 

But for "Sterling Retail," I’m seeing triple the ARR I expected. 

**dan.lee** — 1:42 PM
You’re getting a fan-out. Are you joining on `customer_id` without filtering for a point-in-time? 

`fact_subscriptions` contains the entire history of every plan change. If Sterling Retail upgraded from Pro to Business and then added seats three times, they’ll have 5 rows in that table. 

If you just want "today," you MUST use `WHERE is_current = true`. 

If you want a historical snapshot (like "what was their MRR on 2025-05-01"), you need to filter:
`WHERE start_date <= '2025-05-01' AND (end_date > '2025-05-01' OR end_date IS NULL)`

**elena.rossi** — 1:45 PM
Ugh, right. I forgot `fact_subscriptions` is an SCD2-style table now. 

Wait, if `is_current` is true, can I trust `mrr_usd`? I see some rows where `mrr_usd` is 0 but the `plan_tier` is 'Business'. 

**dan.lee** — 1:50 PM
Check the `customer_id`. Is it one of the trial accounts or a partner? Some of the legacy "Beta" partners are on the Business tier but have a 100% discount applied in Stripe, which flows through as 0 MRR. 

Try this to exclude the noise:
`SELECT sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = true AND mrr_usd > 0`

**elena.rossi** — 2:05 PM
That fixed it. Also, "Global Dynamics" shows a `change_type` of `'churn'` but their `status` in `dim_customers` is still `'active'`. Which one is the source of truth?

**dan.lee** — 2:10 PM
`dim_customers.status` is synced from the CRM (Salesforce) every 4 hours. `fact_subscriptions` is synced from the billing system (Stripe) daily. 

If they cancelled their subscription but their contract technically hasn't ended yet, the CRM might still show them as active until the end of the month. Use `dim_customers` for "Who is our customer today?" and `fact_subscriptions` for "Are they actually paying us right now?"

---

# #data-help — 2026-05-08

**omar.sharif** — 9:15 AM
Quick question for the data folks—I'm looking for the "VRS" (Value Realization Score) for the Enterprise accounts. Is that in a flat table yet? 

**dan.lee** — 9:20 AM
Not in a flat table yet. It’s still calculated in a legacy dbt model because the logic is... sensitive. 

It’s basically: `(fact_workflow_runs in last 30d) / (seat_count * 10)`. 

If you need it for a QBR, you can approximate it using `fact_workflow_runs`. 

```sql
SELECT 
  customer_id, 
  COUNT(run_id) as total_runs
FROM nexus-analyst-demo.acme.fact_workflow_runs
WHERE triggered_at >= CURRENT_DATE - 30
GROUP BY 1
```

Join that to `dim_customers` to get the `account_tier`. We generally consider anything > 50 runs per licensed seat as "Healthy."

**omar.sharif** — 9:25 AM
Perfect. I have a meeting with "Velocity Tech" at 11:00. They’re Enterprise but I have a feeling their usage dropped after they cut their DevOps team last month. 

**rajiv.menon** — 10:00 AM
@dan.lee sorry to be a pain, but the `acquisition_channel` in `dim_customers` for the last batch of signups is all `NULL`. 

**dan.lee** — 10:05 AM
Let me check the ingestion logs... 
Ah, it looks like the Segment integration for the new "Spring Promo" landing page wasn't passing the UTM parameters to the `user_events` table. 

Marketing changed the URL structure without telling us. Again. 

I’ll have to manually patch the `acquisition_channel` for about 400 rows in `dim_customers`. It’ll be fixed in the 2:00 PM warehouse refresh.

**rajiv.menon** — 10:07 AM
😬 My bad. I think that was the agency we hired for the EMEA launch. I'll make sure they use the canonical tagging template next time.

---

# #ops-announcements — 2026-05-08

**dan.lee** — 4:00 PM
**BI UPDATE:** The `fact_user_events` table is now partitioned by `event_date`. 

If you are running a query like `SELECT * FROM nexus-analyst-demo.acme.fact_user_events`, it will now FAIL unless you include a date filter. We are doing this to save on BigQuery costs because some of you are scanning 4TB of data just to find out how many times someone clicked "Settings" yesterday. 

**Example of the RIGHT way to do it:**
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE event_at >= '2026-05-01'`

**Example of the WRONG way:**
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_user_events` (This will cost us $20. Don't do it.)

Also, we added a new column: `app_version`. This will help the product team track the rollout of the new Workflow Designer.

---

# #data-help — 2026-05-09

**elena.rossi** — 11:30 AM
Does anyone know why `dim_users.is_active` would be `true` but `last_login_date` is `NULL`? 

**dan.lee** — 11:35 AM
Those are "invited" users who haven't accepted the invite yet. 

In `dim_users`: 
- `is_active` = they have a seat provisioned (and we are likely charging for it if they are on a Business/Pro plan).
- `last_login_date` = NULL means they haven't actually authenticated yet. 

If you’re doing an "Active User" count for Marcus, you should probably filter for `last_login_date >= CURRENT_DATE - 30`. We have about 2,000 users who are "active" in the billing sense but have never actually logged in. 

**elena.rossi** — 11:40 AM
That changes my Engagement Rate by like 12%. Wow. 

**dan.lee** — 11:42 AM
Yeah. Welcome to the "Seat Recycler" project. CS is going to use that data to tell customers to de-provision those seats so they can save money, which helps with NRR but hurts Gross Bookings. It's a whole thing.

# #random — 2026-05-09

**ben.wu** — 12:05 PM
Is the Blue Bottle on 2nd still doing that weird lavender latte? Asking for a friend (the friend is me). ☕

**sarah.jenkins** — 12:10 PM
Yeah, but the line is out the door. Better off going to the pantry and using the Jura. I think someone finally refilled the espresso beans.

**rajiv.menon** — 12:15 PM
FYI for the SF team — the 4th floor micro-kitchen is closed for "deep cleaning" until 3 PM. Don't be the person who tries to microwave fish in the 3rd floor one. We all remember the Incident of '25.

---

# #data-help — 2026-05-10

**sarah.jenkins** — 9:30 AM
I’m trying to pull a list of customers for the Q2 EBRs and my NRR calculation is coming out to 155% for the Business tier. That feels... wrong? Even for us. 

I’m joining `nexus-analyst-demo.acme.dim_customers` to `nexus-analyst-demo.acme.fact_subscriptions`. 

**dan.lee** — 9:45 AM
@sarah.jenkins You’re probably double-counting the upgrade rows. `fact_subscriptions` keeps a history of every change. 

If a customer moved from Pro to Business in April, they have TWO rows for that month if you aren't filtering. 

You need to add `WHERE is_current = TRUE` if you want the current snapshot, OR if you are doing historical NRR, you have to group by `customer_id` and `date_trunc(start_date, MONTH)`. 

Also, check your `change_type`. If it’s 'churn', the MRR goes to 0 but the row stays there.

**sarah.jenkins** — 10:02 AM
Ugh, okay. Let me try again. 

`SELECT sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = TRUE`

Wait, now I’m getting $3.1M for total MRR. Is that right?

**dan.lee** — 10:05 AM
Check the canon doc. Total ARR is ~$39M. $3.1M MRR * 12 = $37.2M. You’re missing the Enterprise deals that are billed annually and haven't been normalized in that specific view yet. 

Use `nexus-analyst-demo.acme.dim_customers.current_mrr_usd` for a quick health check. It’s a flattened field that Finance (Chloe) reconciled yesterday.

---

# #ops-announcements — 2026-05-11

**chloe.pham** — 2:15 PM
**FINANCE ALERT:** We are seeing a mismatch in "Bookings" vs "MRR" for the recent Hooli expansion. 

Sales logged it as a $120k expansion (ACV), but because they have 3 months of "ramp credits," the actual MRR impact in `fact_subscriptions` won't show up until August. 

If you are building dashboards for the Board Meeting, please use the `fact_invoices` table to see "Cash Collected" vs `fact_subscriptions` for "Contracted Revenue." 

And for the love of god, stop using `amount_usd` from invoices to calculate churn. Invoices include sales tax and one-time implementation fees. Use `mrr_usd`.

---

# #data-help — 2026-05-12

**elena.rossi** — 11:15 AM
Does anyone have the logic for the **VRS (Value Realization Score)**? 

Marcus wants to see which Enterprise accounts are "under-utilizing" their quota before the renewal cycle starts.

**dan.lee** — 11:22 AM
VRS isn't in a table yet (thanks, Eng backlog). You have to calculate it manually:

1. Sum `step_count` from `nexus-analyst-demo.acme.fact_workflow_runs` for the last 30 days per `customer_id`.
2. Divide by `workflow_run_quota_per_month` from `dim_plans` (joined via `plan_tier`).
3. If they are > 80%, they are "Healthy." If they are < 20%, they are "At Risk."

Note: `fact_workflow_runs` is HUGE. Please filter by `triggered_at >= '2026-04-01'`. If you scan the whole history, the BigQuery billing alert will wake me up at night.

**elena.rossi** — 11:30 AM
Got it. Is there a reason why `status` in `fact_workflow_runs` has 'failed' but the `step_count` is still > 0?

**dan.lee** — 11:32 AM
Yeah, a workflow can run 5 steps and then fail on the 6th. We still count those steps against their quota because our workers did the compute. 

**rajiv.menon** — 11:45 AM
Wait, we charge for failed runs? 😅

**dan.lee** — 11:46 AM
Welcome to B2B SaaS, Rajiv.

---

# #random — 2026-05-12

**marcus.obrien** — 1:00 PM
Found a Hydro Flask in the "Auckland" conference room. It has a sticker that says "Data Is The New Oil." 

I'm leaving it at the front desk. Also, please stop naming conference rooms after cities we don't have offices in. It's confusing the candidates.

**sarah.jenkins** — 1:05 PM
That's definitely Dan's bottle. 

**dan.lee** — 1:10 PM
Guilty. And "Auckland" is a great city. We should open an office there. Think of the latency benefits for APAC customers. 🇳🇿

---

# #data-help — 2026-05-13

**elena.rossi** — 4:00 PM
Found a weird bug in `dim_users`. 

I have a user `user_id: 99283` associated with `customer_id: 441` (Initech), but their `email_domain` is `gmail.com`. I thought we enforced corporate domains for Business tier?

**dan.lee** — 4:05 PM
We do for *new* signups. But if an admin invites them via `invited_by_user_id`, the validation is softer. 

Initech has a lot of contractors. Check `role` in `dim_users`. If it's 'external_contributor', that explains the Gmail address. 

Also, HEY—anyone looking at the `fact_user_events` for the new Workflow Designer? The `event_at` timestamp for yesterday is showing a massive spike at 3 AM UTC. 

**rajiv.menon** — 4:10 PM
That was the EMEA launch event. We had about 400 people in London and Amsterdam live-testing the beta concurrently.

**dan.lee** — 4:12 PM
Okay, cool. Just making sure it wasn't a bot crawl. `nexus-analyst-demo.acme.fact_user_events` is showing 1.2M rows for that hour alone. 

By the way, I'm deprecating `dim_customers.region` in favor of `dim_customers.country` mapped to a new `geo_mapping` seed file next week. Update your Looker explores accordingly.

# #data-help — 2026-05-14

**elena.rossi** — 9:15 AM
Is anyone else seeing weird NRR (Net Revenue Retention) numbers for the MM (Mid-Market) segment in the Executive Dashboard? I’m getting 142% for April, which seems... suspiciously high even for us.

**dan.lee** — 9:22 AM
@elena.rossi Check your join logic on `nexus-analyst-demo.acme.fact_subscriptions`. Are you filtering for `is_current = true`? If you just sum `mrr_usd` without handling the `change_type`, you’re probably double-counting the expansion MRR and the base MRR for the same `customer_id` in the same month.

**chloe.wang** — 9:30 AM
Elena, also check if you're including the Globex Corp expansion. They moved from Business to Enterprise on April 12th. That was a huge jump—about $12k in expansion MRR alone. 

**elena.rossi** — 9:45 AM
Ah, I see it. I wasn't accounting for the `changed_from_subscription_id` logic. I was just doing a sum of `mrr_usd` grouped by `month`. 🤦‍♀️

**dan.lee** — 9:47 AM
Standard mistake. Also, remember that `dim_customers.account_tier` is a SCD (Slowly Changing Dimension) but we’re only storing the *current* state in the flat table. If you want to see what tier they were in April 2025, you have to look at the `plan_tier` in `fact_subscriptions` at that timestamp. 

---

# #random — 2026-05-15

**marcus.obrien** — 11:00 AM
The espresso machine in the SF office is leaking again. Please don't try to "fix" it by jamming a folded napkin under the tray. Looking at you, Engineering.

**rajiv.menon** — 11:05 AM
I feel targeted. Also, the napkin works.

**sarah.jenkins** — 11:10 AM
Can we get more oat milk? We’re down to the last carton of the "Barista Edition" and people are starting to look feral.

---

# #data-help — 2026-05-16

**chloe.wang** — 2:30 PM
Quick question for the data folks—why does `nexus-analyst-demo.acme.dim_customers` show `seat_count_licensed` as 0 for some of our oldest customers (like Cyberdyne Systems)? They definitely have users.

**dan.lee** — 2:35 PM
Legacy debt. Cyberdyne signed in Jan 2023 when we were still manual-provisioning everything via the backend. The `seat_count_licensed` field wasn't enforced in the DB until the Series A revamp in Q4 '24. 

If it's 0, use `count(user_id)` from `dim_users` as a proxy, or check the `fact_invoices` for the last `amount_usd` divided by the seat price. But honestly, just look at `fact_subscriptions.seat_count`. That's the source of truth for billing.

**elena.rossi** — 2:40 PM
Wait, if `fact_subscriptions.seat_count` is the truth, why do we even have it in `dim_customers`?

**dan.lee** — 2:42 PM
Because Sales wants a "one-stop shop" table and they hate doing joins. 🤷‍♂️

---

# #data-help — 2026-05-19

**sarah.jenkins** — 10:15 AM
I'm trying to build a "churn risk" cohort. What’s our official definition of an "Inactive User"? 

**rajiv.menon** — 10:18 AM
For CS, it's anyone who hasn't logged in for 14 days. 

**dan.lee** — 10:20 AM
Actually, the "Engagement Score" we built last month uses `nexus-analyst-demo.acme.fact_user_events`. 

An "active" user is defined as having at least one `event_id` where `event_type` is 'workflow_published' or 'workflow_test_run' in the last 30 days. Just looking at `last_login_date` in `dim_users` is misleading because people leave the dashboard open in a tab for weeks.

**sarah.jenkins** — 10:25 AM
Got it. So if I join `dim_users` to `fact_user_events`, I should filter for those specific event types?

**dan.lee** — 10:27 AM
Exactly. And filter out `customer_id = 1` (that’s us, Acme internal). Our own testing spikes will ruin your averages. We run like 50k workflows a day just testing the staging environment.

---

# #random — 2026-05-20

**marcus.obrien** — 12:05 PM
Lunch is here. Tacos from "The Alchemist." 🌮

Please note: The "Extra Spicy" salsa is not a joke. I saw a junior dev cry during the last All-Hands.

**dan.lee** — 12:10 PM
Challenge accepted. 

**elena.rossi** — 12:15 PM
Dan, don't. You have a board prep meeting at 1 PM. You can't be sweating through your shirt while explaining the NRR dip.

**dan.lee** — 12:16 PM
"NRR dip" is a strong phrase. I prefer "Seasonal variance in expansion velocity."

**chloe.wang** — 12:17 PM
Spoken like a true executive. See you in the Auckland room at 1:00. 🇳🇿

# #data-help — 2026-05-21

**sarah.jenkins** — 9:45 AM
Quick check on NRR for the Board Deck—I'm seeing 124% for the MM segment in April, but Finance is reporting 118%. I’m pulling from `nexus-analyst-demo.acme.fact_subscriptions`.

**dan.lee** — 9:50 AM
Are you filtering for `change_type`? If you just sum `mrr_usd` from that table without looking at the cohort start, you're going to include New Business ARR in the numerator. NRR should only look at expansion, contraction, and churn from the *existing* base at the start of the period.

**sarah.jenkins** — 9:55 AM
Ah, I was just doing `SUM(mrr_usd) WHERE month = '2026-04-01' / SUM(mrr_usd) WHERE month = '2025-04-01'`. 

**dan.lee** — 9:58 AM
Yeah, that's "Total Revenue Growth," not NRR. You need to join the April 2026 snapshot back to the April 2025 customer list. Also, check if you're excluding `customer_id` 442 (Global Corp). They had that weird mid-month tier jump from Business to Enterprise that creates a double-entry in `fact_subscriptions` if you don't filter for `is_current = true`.

**elena.rossi** — 10:05 AM
Also, Sarah, make sure you aren't counting the "Paused" accounts as churned. Sales is still fighting for those. Filter `status` in `dim_customers` for 'Active' or 'Paused' specifically if you want the "Gross Retention" view vs "Net Retention."

---

# #random — 2026-05-21

**marcus.obrien** — 10:15 AM
The espresso machine in the 4th-floor breakroom is making a sound like a dying jet engine. Proceed with caution. ☕️🚀

**rajiv.menon** — 10:17 AM
Is that why my latte tasted like burnt rubber?

**chloe.wang** — 10:20 AM
That's just the "Dark Roast" Marcus bought. He says it tastes like "productivity," I say it tastes like charcoal.

---

# #data-help — 2026-05-22

**rajiv.menon** — 11:30 AM
I’m looking at `nexus-analyst-demo.acme.fact_workflow_runs` to see why "Velocity Tech" (customer_id 881) is hitting their quota limits so early. It says they’ve had 95k runs this month, but they only have 20 users?

**dan.lee** — 11:35 AM
Check their `event_type` in `fact_user_events`. I bet they have a loop running on a 1-minute cron. If `step_count` in `fact_workflow_runs` is low (like 1 or 2) but `run_id` count is high, it’s usually a heartbeat check that they forgot to turn off.

**rajiv.menon** — 11:38 AM
Found it. They have a workflow called 'Slack-Bot-Ping' that's been failing every 30 seconds since Tuesday. `error_code` is '401-Unauthorized'. 

**dan.lee** — 11:40 AM
Oof. Tell their CSM to have them fix the API key. We’re billing them $149/seat for Business tier, but they’re burning through their 100k run quota on garbage data. If they hit the limit, the platform will auto-throttle them, and then they'll complain the "product is broken."

---

# #ops-announcements — 2026-05-22

**chloe.wang** — 2:00 PM
Friendly reminder: Monday is a bank holiday in EMEA. The Amsterdam office will be closed. 🇳🇱

For the US team, we’re still on for the "Summer Kickoff" BBQ at 4 PM on the roof deck. Please update the poll in #social if you want the vegan burger option so Marcus can get the count right.

---

# #data-help — 2026-05-23

**elena.rossi** — 9:15 AM
I'm seeing a discrepancy in `dim_customers.current_mrr_usd`. For "Skyline Logistics," it says $7,450, but their plan is Business tier with 60 seats. Shouldn't it be $8,940? (60 * $149)

**dan.lee** — 9:20 AM
Check `fact_subscriptions` for that `customer_id`. They probably have a "Legacy Discount" or a "Volume Negotiated Rate." 

Actually, I just looked—Skyline is on a custom Enterprise contract that we haven't fully migrated to the automated billing engine yet. Their `account_tier` is 'Enterprise' but their `current_plan_tier` is still 'Business' because they haven't enabled SSO. 

**elena.rossi** — 9:22 AM
Ugh, "Plan" vs "Tier" is going to be the death of me. So `dim_customers.account_tier` is what Sales cares about, but `fact_subscriptions.plan_tier` is what actually gets billed?

**dan.lee** — 9:25 AM
Bingo. Join on `customer_id` and always trust the `fact_subscriptions.mrr_usd` for actual dollars. The `dim_customers` version is just a denormalized convenience field and it lags by 24 hours.

**sarah.jenkins** — 9:30 AM
Is that why my "Top 10 Customers" query returned 11 rows yesterday? 

**dan.lee** — 9:31 AM
Probably. If you don't filter for `is_current = true` in `fact_subscriptions`, you'll get the old row AND the new row if they upgraded mid-month. The "Flat" tables are only flat if you use the right filters, lol. 

Query should look like:
`SELECT * FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current IS TRUE`

**sarah.jenkins** — 9:35 AM
Adding that to the "Data Gotchas" Wiki page now. 📝

---

# #random — 2026-05-23

**marcus.obrien** — 12:15 PM
The "The Alchemist" tacos are back, but I ordered the mild salsa this time. I can't have Dan passing out again before the EOM sync.

**dan.lee** — 12:18 PM
I didn't "pass out," I was "meditating on the spice profile." 🧘‍♂️🌶️

# #data-help — 2026-05-24

**rajiv.shah** — 10:45 AM
Hey team, I’m trying to pull NRR (Net Retention Rate) for the MM (Mid-Market) cohort that signed in Q2 2025. My query is giving me like 215% which... I mean, I’m a great AE, but that seems physically impossible for that segment. 😅

**dan.lee** — 10:50 AM
@rajiv.shah Are you joining `fact_subscriptions` to itself to get the starting MRR vs. ending MRR? If you just sum `mrr_usd` over the whole year without a date filter, you're triple-counting every time someone added seats or changed plans.

**rajiv.shah** — 10:52 AM
I'm using `nexus-analyst-demo.acme.fact_subscriptions` and joining on `customer_id`. 

**elena.rossi** — 10:55 AM
That's the issue. If "Velocity Tech" upgraded 3 times in 12 months, you're seeing 4 rows for them in the join. You need to anchor the "Start" MRR to a specific `subscription_id` or date. 

Try this:
`SELECT customer_id, mrr_usd FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current IS TRUE` 
Wait, actually for NRR you need the historical row. Use `end_date` to find the record that was active exactly 12 months ago.

**dan.lee** — 11:02 AM
Also Rajiv, check your `account_tier` filter. Some of those "MM" accounts were "SMB" when they signed and moved up. If you filter by *current* tier in `dim_customers`, you're getting survivorship bias. You want their tier *at the time of the start date*.

**rajiv.shah** — 11:05 AM
My head hurts. Can we just get a `fact_retention` table? 

**dan.lee** — 11:06 AM
It’s on the roadmap for Q3. For now, just use the `change_type` column in `fact_subscriptions` to isolate 'Expansion' vs 'Contraction'.

---

# #random — 2026-05-24

**marcus.obrien** — 1:15 PM
Whoever left the half-eaten tuna melt in the micro-kitchen: please, for the love of God, the Dutch office doesn't smell this bad and they eat pickled herring. 🤢

**sarah.jenkins** — 1:20 PM
It was probably the Eng team during the sprint finish. They've been living in the "Nexus" conference room for 48 hours.

---

# #data-help — 2026-05-25

**chloe.kim** — 9:40 AM
Quick check: Does `fact_workflow_runs` include deleted workflows? I’m looking at "Global Health Net" and their run count dropped to zero on Friday, but they haven't churned.

**alex.chen** — 9:45 AM
The `fact_workflow_runs` table shows *execution* logs. If the workflows were deleted, they won't show up. Check `dim_customers.status`—if they’re still 'Active', they might just be reconfiguring their integrations. 

**chloe.kim** — 9:48 AM
They have 400 seats licensed! If they aren't running workflows, that's a massive churn risk. 

**elena.rossi** — 9:50 AM
@chloe.kim Check `fact_user_events`. See if anyone from the `globalhealth.org` domain has logged in. Sometimes they pause the automations during an internal audit. 

**chloe.kim** — 10:05 AM
Found it. High `event_type = 'integration_error'` in `fact_user_events` right before the drop. Looks like their OAuth token for Salesforce expired and no one noticed. Pinging their admin now. Data saves the day again. 🚀

---

# #random — 2026-05-25

**dan.lee** — 11:15 AM
The espresso machine is making that high-pitched whistling sound again. I think it’s trying to communicate in SQL.

**marcus.obrien** — 11:17 AM
`SELECT caffeine FROM tank WHERE temperature > 90`

**dan.lee** — 11:18 AM
`ERROR: Out of Beans Exception`

---

# #data-help — 2026-05-26

**sarah.jenkins** — 2:10 PM
Help! Trying to calculate Gross Bookings for the Board Deck. Should I sum `amount_usd` from `fact_invoices` or annualize `mrr_usd` from `fact_subscriptions`? 

**elena.rossi** — 2:15 PM
Depends on the metric. 
Finance wants `fact_invoices` for GAAP Revenue/Cash. 
Sales/Product usually wants "Annualized Run Rate" (ARR) which is `fact_subscriptions.mrr_usd * 12`. 

Just be careful with the `billing_cycle`. If you sum `amount_usd` from invoices, you’ll see huge spikes in months where the Annual contracts renew, and nothing for the other 11 months.

**sarah.jenkins** — 2:20 PM
Right, okay. I'll stick to `fact_subscriptions`. 
Wait, I see some rows where `mrr_usd` is $0 but `seat_count` is 50. Is that a bug?

**dan.lee** — 2:25 PM
Not a bug. Those are usually "Partner" accounts or "Internal" testing accounts. Filter out `customer_id` where `acquisition_channel = 'Internal'` or check `dim_customers.status = 'Active'`. 

Also, we have a few 'Free' tier customers who have 100 seats but $0 MRR. They’re on an extended trial.

**sarah.jenkins** — 2:30 PM
Got it. 
`WHERE mrr_usd > 0 AND is_current IS TRUE`
...and excluding 'Acme Inc' as a customer. Done. Thanks!

---

# #random — 2026-05-26

**marcus.obrien** — 4:00 PM
Reminder: Amsterdam office is closed tomorrow for King's Day! 🇳🇱 🧡 Expect delays if you're waiting on the EMEA team for anything. 

**rajiv.shah** — 4:05 PM
Wait, does that mean no one is monitoring the `vrs-production-v2` status?

**alex.chen** — 4:07 PM
I've got the on-call pager for the holiday. Don't worry Rajiv, your precious leads are safe. 🛡️

# #data-help — 2026-05-27

**sarah.jenkins** — 9:45 AM
Hey team, I’m trying to pull Net Revenue Retention (NRR) for the Enterprise segment for Q1. My numbers are looking... too good? Like 140%. I think I'm double counting upgrades. 

Here is my join: 
`SELECT sum(a.mrr_usd) as beginning, sum(b.mrr_usd) as ending`
`FROM nexus-analyst-demo.acme.fact_subscriptions a`
`JOIN nexus-analyst-demo.acme.fact_subscriptions b ON a.customer_id = b.customer_id`
`WHERE a.is_current IS FALSE AND b.is_current IS TRUE`

**elena.rossi** — 9:52 AM
@sarah.jenkins Yeah, that join is going to explode if a customer had multiple plan changes in the period. You're joining every historical row to the current row. 

You should use `change_type` to track the delta or just snapshot the MRR at the start of the quarter vs the end of the quarter using `dim_dates`. 

Also, are you filtering for `account_tier = 'Enterprise'` in `dim_customers`? If you use the tier from `fact_subscriptions`, it might have changed mid-quarter. 

**sarah.jenkins** — 10:05 AM
Ah, good point on the tier change. If they moved from Business to Enterprise in Feb, they should be in the 'Expansion' bucket for the Enterprise cohort, or do they stay in Business for the NRR calc? 

**dan.lee** — 10:10 AM
Finance usually counts them based on the tier they were in at the *start* of the period. Check the `finance_v3_mart` documentation (wait, ignore that, we moved it to the flat schema). 

Just use:
`SELECT * FROM nexus-analyst-demo.acme.dim_customers WHERE account_tier = 'Enterprise'` 
...as your base set, then look at their `fact_subscriptions` MRR on 2026-01-01 vs 2026-03-31. 

**sarah.jenkins** — 10:15 AM
Got it. Also, I see `change_type = 'Churn'` for 'DataViz Corp' but their `status` in `dim_customers` is still 'Active'. What gives?

**dan.lee** — 10:18 AM
Check the `end_date`. They probably set their subscription to cancel at the end of the period, but the period hasn't ended yet. They have access until June 1st. 

---

# #random — 2026-05-27

**marcus.obrien** — 12:05 PM
Is it just me or is the AC in the SF office set to "Arctic Tundra" today? I'm wearing a hoodie and a parka.

**rajiv.shah** — 12:07 PM
Facilities said the sensor is broken. It thinks there are 200 people in the lounge. 

**marcus.obrien** — 12:10 PM
If only we had a sensor that could trigger a workflow to turn it down. `IF temp < 65 THEN heat_up`. 

**alex.chen** — 12:12 PM
We’d need the Nest integration for that. Too bad the API is still in beta for our platform. 😅

---

# #data-help — 2026-05-28

**rajiv.shah** — 11:30 AM
Quick question on `fact_workflow_runs`. I’m trying to find "Stale" customers—those who haven't run a workflow in 14 days. 

Is `triggered_at` in UTC or local? 

**elena.rossi** — 11:32 AM
Everything in `nexus-analyst-demo.acme` is UTC. 

**rajiv.shah** — 11:35 AM
Cool. Also, does `status = 'Error'` count as usage? Some of these accounts have 1,000 runs but they're all 403 errors because their credentials expired. 

**dan.lee** — 11:40 AM
For the "Active User" metric, we usually only count `status = 'Success'`. 
If you’re looking for churn risk, the high error rate is actually a better signal than no usage at all. It means they *want* to use it but it's broken. 

Try this:
`SELECT customer_id, count(*) as error_count`
`FROM nexus-analyst-demo.acme.fact_workflow_runs`
`WHERE status != 'Success' AND triggered_at > CURRENT_DATE() - 7`
`GROUP BY 1`

**rajiv.shah** — 11:45 AM
Found a huge spike for 'LogisticsPlus'. 99% error rate since Tuesday. 

**alex.chen** — 11:48 AM
@rajiv.shah LogisticsPlus is on the `vrs-production-v2` cluster. We had a deployment issue with the DHL connector on Tuesday. It’s a known bug. Fix is rolling out now.

---

# #random — 2026-05-29

**dan.lee** — 9:00 AM
Standup in 5 mins. Bring your own coffee, the machine is still whistling the Imperial March. ☕️

---

# #data-help — 2026-05-29

**sarah.jenkins** — 3:00 PM
Last one for the week—I'm looking at `dim_users` and I see a lot of `invited_by_user_id` is NULL. Does that mean they are the Account Owner?

**elena.rossi** — 3:05 PM
Not necessarily. It usually means they signed up via SSO or were the very first user created when the account was provisioned. 

If you want the Owner, join to `dim_customers` and look at the `acquisition_channel`. If it was 'Sales-Led', the first user is usually the admin who signed the contract. 

**sarah.jenkins** — 3:10 PM
Wait, I’m seeing `user_id` 88291 associated with 4 different `customer_id`s. Is that possible? 

**dan.lee** — 3:12 PM
Yep. Consultants. They get invited to multiple Acme instances to manage workflows for their clients. 
The `nexus-analyst-demo.acme.dim_users` table is unique on `user_id`, but a user can have multiple entries in `fact_user_events` across different `customer_id` contexts. 

Actually, wait—in the FLAT schema, `dim_users` should show their "primary" customer. If you need the mapping of users to all customers, you have to use the `fact_user_event` logs to see where they are actually active. 

**sarah.jenkins** — 3:15 PM
Data is never as clean as the ERD suggests, is it? 

**dan.lee** — 3:16 PM
If it were clean, they wouldn't need us. 🫡

**marcus.obrien** — 4:45 PM
Happy Friday everyone! Amsterdam team is already offline (and probably halfway to a canal boat). See you all Monday! 🍻

---

# #random — 2026-06-01

**dan.lee** — 8:45 AM
Welcome back everyone. Hope the weekend was better than the build logs. 
Reminder: The 4th floor fridge is being cleaned at 4 PM today. Anything without a name on it is getting sent to the void. Including that half-eaten burrito that's been there since the Series B party.

**sarah.jenkins** — 9:02 AM
Is the coffee machine still playing the Star Wars theme?

**dan.lee** — 9:05 AM
Office Ops says the part is on backorder. Embrace the dark side, Sarah. ☕️

---

# #data-help — 2026-06-01

**marcus.obrien** — 10:15 AM
Hey team, I'm trying to pull NRR (Net Revenue Retention) for the MM (Mid-Market) segment for May. My numbers are looking... suspiciously high. Like 240% high. I think I'm double counting something. 

Here’s my logic:
`SELECT sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE customer_id IN (SELECT customer_id FROM nexus-analyst-demo.acme.dim_customers WHERE account_tier = 'MM')`

**elena.rossi** — 10:22 AM
@marcus.obrien Yeah, you're definitely double counting. `fact_subscriptions` contains the *entire history* of every sub change for a customer. If a customer upgraded three times in May, you're summing all three records. 

You need to filter for `is_current = TRUE` if you want the "now" state, or more likely for NRR, you need to compare the MRR at the start of the month vs the end of the month for the same cohort of `customer_id`s.

**dan.lee** — 10:25 AM
Marcus, also check the `change_type`. If someone moved from 'Pro' to 'Business', you'll see an 'upgrade' record and the 'original' record might still show up in your sum if you don't filter by `end_date` or `is_current`. 

**sarah.jenkins** — 10:30 AM
Wait, if I want to see "Expansion MRR" for last month, should I look at `fact_subscriptions` where `change_type = 'upgrade'`? 

**elena.rossi** — 10:34 AM
Exactly. But be careful—some 'upgrades' are just seat expansions, while others are tier jumps (e.g., Pro -> Business). Check the `plan_tier` column to differentiate. 

---

# #data-help — 2026-06-02

**rajiv.shah** — 1:15 PM
Quick check—what’s our canonical definition for an "Active User"? 
I’m seeing a discrepancy between the dashboard and my query on `nexus-analyst-demo.acme.dim_users`.

**dan.lee** — 1:20 PM
`dim_users.is_active` just means the account isn't deactivated/deleted. 
For "Engaged Users" (what the board looks at), we use `fact_user_events`. 

Canonical DAU/MAU is:
`SELECT count(distinct user_id) FROM nexus-analyst-demo.acme.fact_user_events WHERE event_at > [TIMESTAMP]`

Usually we filter for "meaningful" events like `workflow_created`, `workflow_edited`, or `run_triggered_manual`. If they just log in and stare at the dashboard, we don't count them as "active" for the engagement metric.

**rajiv.shah** — 1:25 PM
Got it. So `login` events are excluded from the "Power User" calc?

**dan.lee** — 1:28 PM
Correct. If they aren't running workflows, they aren't sticky. 

---

# #random — 2026-06-03

**alex.chen** — 12:10 PM
Taco Tuesday is happening at "The Local" because the truck didn't show up. Meet at the lobby in 5. 🌮

---

# #data-help — 2026-06-04

**sarah.jenkins** — 11:00 AM
I’m looking at `fact_subscriptions` and trying to annualize the bookings for 'CloudScale Inc'. 
They have a `mrr_usd` of $4,500 but their `billing_cycle` says 'annual'. Is the $4,500 the monthly equivalent or the total invoice amount? 

**elena.rossi** — 11:05 AM
In the `nexus-analyst-demo.acme` FLAT tables, `mrr_usd` is *always* normalized to monthly. 
So if they are on an annual plan, their total contract value (TCV) is `mrr_usd * 12`. 

**sarah.jenkins** — 11:08 AM
Okay, that makes sense. So for 'CloudScale Inc', the annual booking was $54k. 

Wait... I just checked `fact_invoices`. They were only billed $48,000 last year. Why the gap? 

**dan.lee** — 11:12 AM
Check `dim_customers`. CloudScale is an Enterprise account. They probably had a "ramp up" period or a multi-year discount that isn't reflected in the flat `mrr_usd` field which just shows the *current* monthly value of the active sub. 

For the actual cash-in-door, always trust `fact_invoices`. For "Run Rate", use `fact_subscriptions`.

**marcus.obrien** — 11:15 AM
CloudScale had a 10% 'Early Adopter' discount applied manually by finance. It’s in the Salesforce notes, but I don’t think that field made it into the BigQuery flat schema yet. 

---

# #data-help — 2026-06-04

**rajiv.shah** — 4:20 PM
VRS Status Check: Seeing a lot of `error_code = 'ETIMEDOUT'` for 'DataStream' flows in the last hour. 
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-9921' AND status = 'Failed'`

**alex.chen** — 4:25 PM
DataStream is hitting the Shopify API limits on their end. Not an Acme infrastructure issue. I’ll ping their admin. 

---

# #data-help — 2026-06-05

**sarah.jenkins** — 9:30 AM
Is `dim_customers.acquisition_channel` reliable for the Q1 2025 cohort? I see a lot of 'Unknown'. 

**elena.rossi** — 9:35 AM
Q1 2025 was when we switched from the old Segment implementation to the new internal collector. 'Unknown' usually means the `utm_source` was stripped or they came in via a direct invite link that wasn't tagged. 

If you need to guess, check the `email_domain` in `dim_users`. If it's a big corp (like 'globex.com'), it was almost certainly Sales-Led/Outbound. If it's 'gmail.com' or a small startup, it was probably PLG/Self-Serve. 

**sarah.jenkins** — 9:40 AM
Ugh, okay. I'll do some manual mapping. 
Also, tiny catch—`fact_workflow_runs` has a `triggered_by` column. Is that a `user_id`? 

**dan.lee** — 9:42 AM
Usually, yes. But it can also be 'SYSTEM' for scheduled tasks or 'WEBHOOK' for external triggers. 
If you're joining it to `dim_users`, make sure to handle the non-integer strings or you'll get a join error in BQ. 

**sarah.jenkins** — 9:45 AM
`SAFE_CAST(triggered_by AS INT64)` it is. Thanks Dan! 

**marcus.obrien** — 5:00 PM
Last one out, turn off the lights! Have a great weekend everyone. 🍹

---

# #data-help — 2026-06-08

**marcus.obrien** — 9:15 AM
Hey team, I’m trying to pull NRR for the Board deck. My numbers for the May cohort look way too high (like 140%). 
I’m joining `fact_subscriptions` on itself to compare `mrr_usd` from 12 months ago. 

**rajiv.shah** — 9:22 AM
140% isn't impossible for Enterprise, but for the whole book? Doubtful. 
Are you filtering for `is_current = true` on both sides of the join? If you just join on `customer_id`, you might be double-counting if they had multiple plan changes in a month. 

**marcus.obrien** — 9:30 AM
Ah, I see what happened. I wasn't accounting for the `change_type = 'Churn'`. 
When a sub ends, `fact_subscriptions` gets a new row with `mrr_usd = 0` but my join was still picking up the last positive value. 

**elena.rossi** — 9:35 AM
Pro tip: Use the `nexus-analyst-demo.acme.fact_subscriptions` table and look for `change_type`. 
If you want Net Revenue Retention, you need:
`(Beginning MRR + Expansion + Upgrades - Contraction - Churn) / Beginning MRR`
The `changed_from_subscription_id` column is your best friend for tracking the lineage of a single customer's upgrades.

**marcus.obrien** — 9:45 AM
Got it. Also, does anyone know if "Skyline Systems" (CUST-4402) is actually Business tier? Salesforce says Enterprise but BQ says Business. 

**sarah.jenkins** — 9:47 AM
They're in the middle of a migration. They signed the paper for Enterprise last week (check `dim_customers.account_tier`), but the actual provisioned `current_plan_tier` in the product won't flip until their SSO config is finished. Engineering says Wednesday. 

---

# #random — 2026-06-09

**dan.lee** — 12:05 PM
Blue Bottle run. Anyone want anything? ☕

**alex.chen** — 12:06 PM
Oat milk latte, please! 

**sarah.jenkins** — 12:07 PM
Cold brew! It's too hot for the office AC to keep up today. 

---

# #data-help — 2026-06-10

**alex.chen** — 2:15 PM
VRS Status Check: We’re seeing a massive spike in `fact_workflow_runs` for `customer_id = 'CUST-1022'`. 
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE triggered_at > '2026-06-10 00:00:00'`
It's already at 450k runs today. Their quota is 100k. 

**dan.lee** — 2:20 PM
That's "Aperture Science". They're on a Business plan. Looks like an infinite loop in one of their DataStream flows. 
I'll kill the process. @sarah.jenkins you might want to tell their CSM (I think it's Jamie?) that they're going to see a massive overage warning in their dashboard. 

**sarah.jenkins** — 2:22 PM
On it. Checking `dim_customers`... yup, Jamie Vance is the CSM. 

---

# #data-help — 2026-06-11

**rajiv.shah** — 11:00 AM
Does `fact_user_events` include "View-only" users? I'm trying to calculate DAU/MAU for the Pro tier. 

**elena.rossi** — 11:05 AM
Yes, `fact_user_events` captures every click/pageview. If you want "Active" as in "actually modified a workflow", you need to filter `event_name` for things like 'workflow_created', 'step_added', or 'run_triggered_manual'. 

If you just want "logged in", any event counts. 

**rajiv.shah** — 11:10 AM
Okay. `SELECT count(distinct user_id) FROM nexus-analyst-demo.acme.fact_user_events JOIN nexus-analyst-demo.acme.dim_customers USING (customer_id) WHERE current_plan_tier = 'Pro'`
Wait, I’m getting a `division by zero` error in my aggregation. 

**dan.lee** — 11:12 AM
Check for customers with `seat_count_licensed = 0`. Sometimes the Free-to-Pro transition has a 1-hour lag where the sub is created but the seats aren't provisioned in the metadata yet. Use `NULLIF(seat_count_licensed, 0)`.

---

# #data-help — 2026-06-12

**sarah.jenkins** — 3:30 PM
Quick sanity check on "Bookings". 
Are we annualizing the `mrr_usd` from `fact_subscriptions` for the "New Business" report? 

**marcus.obrien** — 3:35 PM
Yeah, Finance wants everything in ARR. 
`New ARR = (mrr_usd * 12)` for any row where `change_type = 'New'`. 
Just be careful with the `billing_cycle`. We have some old "Quarterly" plans in the `dim_plans` table from 2024 that we don't sell anymore, but some customers like 'Global Dynamics' (CUST-5512) are still on them. The `mrr_usd` column is *already* normalized to monthly, so you don't need to divide by 3 or anything. 

**sarah.jenkins** — 3:40 PM
Perfect. That simplifies things. 
I'm building a Looker dashboard for the AEs to see their "Gap to Quota". 
I'll use `dim_employees` to map the `ae_employee_id` to the actual names. 

**dan.lee** — 3:42 PM
Make sure to filter `dim_employees.is_active = true`. We had some turnover in the EMEA Sales team last month and their old IDs are still in the customer records until the accounts get reassigned. 

**sarah.jenkins** — 3:45 PM
Good catch. I see a few 'CUST-' records assigned to 'EMP-999' (the placeholder for 'Unassigned/House Account'). 

---

# #random — 2026-06-12

**elena.rossi** — 5:05 PM
Happy Friday! Going to the park. 🌳 
Don't forget the dbt full-refresh runs tonight at midnight. The warehouse might be a bit slow if you're trying to pull late-night queries. 

**marcus.obrien** — 5:10 PM
Copy that. Enjoy the sun! ☀️

# #data-help — 2026-06-15

**maya.patel** — 9:45 AM
Hey team, I’m trying to pull the NRR (Net Revenue Retention) for the Board deck. 
I’m looking at `nexus-analyst-demo.acme.fact_subscriptions` but the numbers look slightly higher than what Finance reported last month. 
Are we counting `change_type = 'Reactivation'` as New Business or Expansion?

**marcus.obrien** — 9:52 AM
Finance usually treats Reactivations as New Business if the customer was churned for > 6 months. 
For NRR, we want to look at the cohort from 12 months ago and see their current `mrr_usd` vs then. 
Try this:
`SELECT SUM(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = true` 
And compare it against the same `customer_id` set from June 2025. 

**maya.patel** — 10:05 AM
Got it. Wait, I’m seeing some customers with `mrr_usd` in `fact_subscriptions` that doesn't match `current_mrr_usd` in `dim_customers`. 
Example: 'Cyberdyne Systems' (CUST-1024). 
`dim_customers` says $14,900 but `fact_subscriptions` shows two active rows? 

**dan.lee** — 10:12 AM
Ah, Cyberdyne has a split contract. They have 100 seats on 'Business' for their North Am team and a separate 'Pro' legacy block for their EMEA dev team. 
`dim_customers.current_mrr_usd` is a roll-up (SUM) of all `is_current = true` rows in the subscriptions table. 
The flat table `nexus-analyst-demo.acme.dim_customers` is updated every 4 hours, so it might lag if a seat was added 20 minutes ago.

**maya.patel** — 10:15 AM
That explains it. Cyberdyne is always the outlier. 🙄

---

# #random — 2026-06-15

**elena.rossi** — 12:15 PM
Is it "Taco Tuesday" or is everyone just coincidentally at the truck outside? 🌮

**dan.lee** — 12:17 PM
Definite coincidence. Also, I think they raised the price of the Al Pastor. $14 for two tacos? In this economy? 

**sarah.jenkins** — 12:20 PM
Still cheaper than a seat on our 'Business' plan lol.

---

# #data-help — 2026-06-16

**alex.chen** — 11:30 AM
Does anyone have the query for "Product Qualified Leads"? 
I need to find 'Free' tier customers who have run more than 50 workflows in the last 7 days. 

**sarah.jenkins** — 11:35 AM
You want `nexus-analyst-demo.acme.fact_workflow_runs`. 
Something like:
```sql
SELECT customer_id, count(*) as run_count
FROM nexus-analyst-demo.acme.fact_workflow_runs
WHERE triggered_at >= CURRENT_DATE() - 7
GROUP BY 1
HAVING run_count > 50
```
Then join on `dim_customers` where `current_plan_tier = 'Free'`. 

**alex.chen** — 11:42 AM
Thanks Sarah! 
Wait, I’m getting 0 results for 'Aperture Science' (CUST-8821). I know for a fact they are hammering the API. 

**dan.lee** — 11:45 AM
Aperture is using a custom webhook trigger that bypasses the standard `triggered_by` user logging. 
Check `fact_workflow_runs` for `triggered_by = 'SYSTEM'`. 
Also, verify they haven't upgraded to Pro already. I think Marcus closed that expansion yesterday. 

**marcus.obrien** — 11:48 AM
Yeah, Aperture (CUST-8821) moved to Pro yesterday afternoon. They’re no longer a PQL, they’re a closed-won expansion. 🚀

---

# #data-help — 2026-06-17

**sarah.jenkins** — 9:15 AM
Is `fact_user_events` missing data from the weekend? 
I’m seeing a massive dip in `event_type = 'workflow_created'` starting Friday at 6 PM. 

**dan.lee** — 9:20 AM
Checking the ingestion pipeline... 
Looks like the Segment-to-BigQuery connector stalled. The `nexus-analyst-demo.acme.fact_user_events` table is about 14 hours behind. 
The raw logs are there, but the dbt model `stg_events` failed because of a schema change in the `metadata` JSON field from the front-end release. 

**sarah.jenkins** — 9:25 AM
Classic. Is this going to affect the "Weekly Engagement" report for the Monday standup?

**dan.lee** — 9:30 AM
I’m running a `dbt run --select fact_user_events --full-refresh` now. 
Should be green in 20 mins. 
Avoid querying that table for a bit or you'll get partial results and wonder why our DAU is 4. 

**marcus.obrien** — 9:35 AM
@sarah.jenkins while Dan is fixing that, can you verify the `acquisition_channel` for 'Tyrell Corp' (CUST-3341)? 
It's listed as 'Organic' but the AE says it was a 'Referral'. 

**sarah.jenkins** — 9:40 AM
Checked the `dim_customers` record. The `acquisition_channel` is pulled from the first-touch attribution in the `dim_users` record for the person who created the org. 
The founder of Tyrell Corp signed up via a Google search (Organic) before the AE even touched it. 
We don't overwrite `acquisition_channel` once it's set in the warehouse to preserve the "true" first touch. 

---

# #random — 2026-06-17

**marcus.obrien** — 10:05 AM
Whoever left the half-eaten tuna sandwich in the fridge... we need to talk about "Data Hygiene" in the kitchen. 🐟

**elena.rossi** — 10:10 AM
`DELETE FROM kitchen.fridge WHERE item_name = 'tuna_sandwich' AND freshness_score < 0.2;`

**dan.lee** — 10:12 AM
Query failed: `Access Denied`. You don't have `ADMIN` permissions for the Breakroom.

---

# #data-help — 2026-06-18

**jamie.chen** — 10:45 AM
Hey team, I’m trying to calculate Net Retention (NRR) for the Board Deck. 
When I join `dim_customers` to `fact_subscriptions`, my May NRR is coming out to 142%. That feels... suspiciously high? 
Even with the expansion at 'Stark Industries' (CUST-4492), it shouldn't be that spiked. 

**dan.lee** — 10:52 AM
@jamie.chen check your join logic on `fact_subscriptions`. 
Are you filtering for `is_current = true`? 
If you just join on `customer_id`, you're likely double-counting customers who had a mid-month tier change (like Stark going from Business to Enterprise). 
You'll get two rows for the same period. 

**jamie.chen** — 11:05 AM
Ah, found it. I wasn't accounting for the `change_type` column. 
I was summing MRR from both the old 'Business' record and the new 'Enterprise' record for the same effective date. 
Fixed the query to use `mrr_usd` from the record where `is_current` is true for the snapshot date. 
NRR is now showing 118%. Much more realistic. 

**sarah.jenkins** — 11:10 AM
118% is still great! Is that primarily driven by seat expansion or the new Workflow Add-on?

**jamie.chen** — 11:15 AM
Mostly seat expansion in the MM (Mid-Market) tier. 
'Weyland-Yutani' (CUST-5521) added 150 seats last week. 

---

# #random — 2026-06-18

**elena.rossi** — 12:30 PM
The espresso machine in the SF office is making a sound like a dying workflow engine. 
Can we get a `hotfix` for the milk steamer? ☕️

**marcus.obrien** — 12:35 PM
I’ll open a Jira ticket: `COFFEE-404: Frother Not Found`.

**dan.lee** — 12:40 PM
Closing as `WONTFIX`. Just drink it black like the data team. 

---

# #data-help — 2026-06-19

**marcus.obrien** — 2:15 PM
Quick check on 'Cyberdyne Systems' (CUST-1011). 
They’re asking for our SOC2 Type II and the latest VRS (Vendor Risk Assessment) before they sign the Enterprise upgrade. 
Who has the latest status on their security review? 

**elena.rossi** — 2:20 PM
@marcus.obrien check the `dim_customers` table. 
I updated the `account_tier` notes field (though it's a bit buried in the flat schema). 
Legal cleared the VRS yesterday. 
The SOC2 report is in the "Sales Enablement" folder on Drive. 

**sarah.jenkins** — 2:30 PM
Marcus, just a heads up—if they upgrade, make sure the AE updates the `seat_count_licensed` in Salesforce immediately. 
Last time with 'Initech' (CUST-9901), the sync to BigQuery stalled and the CSM got an automated "Over Quota" alert even though they’d just paid for the extra capacity. 
It makes us look disorganized when the data doesn't flow to `nexus-analyst-demo.acme.dim_customers` fast enough.

---

# #data-help — 2026-06-20

**aarav.gupta** — 9:00 AM
Is there a reason `fact_workflow_runs` doesn't have a `project_id`? 
I’m trying to see which teams within 'Globex Corp' (CUST-7721) are burning through their 100K monthly quota. 

**dan.lee** — 9:15 AM
We don't expose `project_id` in the flat analyst schema to keep the join count down. 
Use `triggered_by` (which is the `user_id`) and join that to `dim_users`. 
From `dim_users`, you can see the `email_domain` or `role` to guess the team. 
If you really need the specific Project container, you have to query the raw `nexus-analyst-demo.acme.stg_workflow_metadata` table, but it's messy. 

**aarav.gupta** — 9:20 AM
Got it. Joining on `user_id` should work for now. 
I just want to make sure we aren't seeing a loop-error. 
Globex had 45,000 runs in the last 4 hours... all with `status = 'failed'` and `error_code = 'ERR_429'`.

**sarah.jenkins** — 9:22 AM
429? That’s rate limiting. 
They’re probably hitting an external API too hard in a `for-each` loop. 
@elena.rossi you might want to ping their admin before their credits hit zero. 

---

# #random — 2026-06-21

**sarah.jenkins** — 4:00 PM
Friendly reminder: Monday is a public holiday for the EMEA team (Midsummer/St. John's Day). 
If you’re waiting on Amsterdam for the Q3 pipeline numbers, you won't get them until Tuesday. ☀️

**marcus.obrien** — 4:05 PM
Wait, does that mean the dbt jobs for the EMEA region will fail if nobody is there to kick them off?

**dan.lee** — 4:10 PM
Marcus... the "A" in "SaaS" doesn't stand for "Always Manual." 
The pipelines are automated. The only thing that stops on Monday is the response time on Slack.

---

# #data-help — 2026-06-22

**jamie.chen** — 11:30 AM
I’m seeing a discrepancy between the `current_mrr_usd` in `dim_customers` and the sum of `mrr_usd` in `fact_subscriptions` for 'Umbrella Corp' (CUST-6612). 
`dim_customers` says $14,900 but `fact_subscriptions` says $12,000. 

**dan.lee** — 11:45 AM
Check the `billing_cycle`. 
Umbrella Corp is on an Annual plan. 
`dim_customers.current_mrr_usd` is a calculated field that annualizes the total contract value and divides by 12. 
`fact_subscriptions.mrr_usd` might be showing the "sticker price" of the base plan before the multi-seat discount was applied. 
Always trust `fact_subscriptions` for the actual transaction-level truth. 
Actually, wait—check if they have a `change_type = 'adjustment'` record. 

**jamie.chen** — 12:00 PM
Found it. There was a credit memo applied last month (invoice `INV-8822`) that wasn't reflected in the `dim_customers` roll-up. 
The flat table `dim_customers` only refreshes its MRR cache once every 24 hours. 
I'll stick to `fact_subscriptions` and `fact_invoices` for the audit. 

**sarah.jenkins** — 12:10 PM
This is why I keep saying we need a `mart_finance_actuals` table. 
The "flat" approach is great for quick counts but dangerous for GAAP reporting. 

**marcus.obrien** — 12:15 PM
As long as the "Booking Annualization" formula doesn't change before the end of the quarter. I need my commission to be accurate! 💰

---

# #data-help — 2026-06-23

**marcus.obrien** — 9:15 AM
Hey team, I'm trying to pull the NRR (Net Revenue Retention) for my territory (West - MM) for the first half of the year. 
When I join `dim_customers` to `fact_subscriptions`, my total MRR is like 3x what it should be. 
Is the `nexus-analyst-demo.acme.fact_subscriptions` table broken? 

**dan.lee** — 9:30 AM
It's not broken, you're just not filtering for the current state. 
`fact_subscriptions` is a SCD (Slowly Changing Dimension) style fact table. It keeps every single historical change. 
If a customer upgraded three times, they have four rows. 
You need to add `WHERE is_current = true` if you want the "now" view, or filter by a specific `start_date` and `end_date` window for point-in-time. 

**marcus.obrien** — 9:45 AM
Ah, okay. So if I want to see what 'Stark Industries' (CUST-4040) was paying in Jan vs now, I have to look at the `change_type`?

**jamie.chen** — 9:50 AM
Exactly. For NRR, use `change_type`. 
`expansion` and `contraction` are your friends there. 
Also, watch out for `Globex Corp` (CUST-1001). They had a weird mid-month migration from Pro to Business that created two 'current' records for about 4 hours before the batch job cleaned it up. 
If you're looking at historical snapshots, always use the `dim_dates` table to join on the last day of the month. 

---

# #random — 2026-06-24

**sarah.jenkins** — 11:00 AM
SF Office: The cold brew tap in the micro-kitchen is spraying foam again. 
Facility team says parts are 2 days out. 
Please don't try to "fix" it by hitting the nozzle. Looking at you, Engineering. ☕️

**dan.lee** — 11:05 AM
I feel targeted. I was just trying to apply some... mechanical pressure.

**marcus.obrien** — 11:10 AM
At least you guys have a tap. Amsterdam is still fighting over the Nespresso pods. 
The "Stark Industries" of coffee problems. 

---

# #data-help — 2026-06-24

**jamie.chen** — 2:30 PM
Quick question on the VRS (Value Realization Score) logic in the new dashboard. 
Are we counting `fact_workflow_runs` where `status = 'error'`? 
'Initech' (CUST-2002) has a high run count, but their error rate is like 40% because of a bad API key. 
If we count those as "active usage," we're overstating their health score. 

**dan.lee** — 2:45 PM
Good catch. The current VRS formula in `nexus-analyst-demo.acme.fact_workflow_runs` just counts total rows. 
We should probably update the engagement threshold. 
I’d suggest: `count(run_id) WHERE status = 'success' AND duration_ms > 100`. 
Short runs (under 100ms) are usually just heartbeats or immediate failures that don't represent actual workflow value. 

**sarah.jenkins** — 3:00 PM
If we change that definition, does it change our "Power User" segment in the marketing tool? 
I’m running a campaign for customers with >1000 successful runs/mo. 

**dan.lee** — 3:15 PM
Yes, it'll drop about 12 customers from that list. 
Most of them are Free tier accounts that are just spamming a webhook anyway. 
I'll update the `mart_customer_health` view tonight. 

---

# #data-help — 2026-06-25

**marcus.obrien** — 10:00 AM
Does anyone know why `current_mrr_usd` for 'Wayne Enterprises' (CUST-5050) is showing as $0 in `dim_customers`? 
They literally signed a $120k ACV Enterprise deal yesterday. 

**dan.lee** — 10:15 AM
Did the deal close in Salesforce? 
The sync to `nexus-analyst-demo.acme.dim_customers` only happens after the `fact_invoices` record is generated. 
Finance has to approve the "Won" status before the billing engine kicks off. 
Check with Ops—if the `paid_at` field in `fact_invoices` is null, the MRR won't roll up to the flat table yet. 

**marcus.obrien** — 10:20 AM
Finance is still waiting on the SOC2 signature from their legal team. 
Ugh. So technically they aren't "active" in the data even if they are already provisioning users?

**jamie.chen** — 10:25 AM
Correct. They'll show up in `dim_users` because they've logged in, but their `status` in `dim_customers` will stay as `pending_onboarding` until that invoice clears. 
You can see their activity in `fact_user_events` though. 
Search for `customer_id = 'CUST-5050'`—it looks like they've already invited 45 users today. 

**marcus.obrien** — 10:30 AM
45 users on a $0 reported MRR. My manager is going to love that report. 🙄

---

# #random — 2026-06-25

**dan.lee** — 12:00 PM
Reminder: The data team is out for a "sync-up" (read: bowling) from 2 PM to 5 PM PT. 
If the warehouse breaks, please contact... actually, just don't break it. 
Check the `#ops-status` channel if the dbt runs look stuck. 🎳

**sarah.jenkins** — 12:05 PM
Last time Dan went bowling, he spent the whole time explaining SQL joins using the bowling pins as entities. 
"The 7-10 split is just a bad outer join," he said. Never again.

# #data-help — 2026-06-26

**carlos.sanchez** — 9:15 AM
Hey team, I’m trying to pull Net Revenue Retention (NRR) for the Board deck. 
When I join `dim_customers` to `fact_subscriptions`, my total MRR for June is coming out to like $14M, which is definitely wrong. 
We should be closer to $3.2M. What am I double-counting? 

**dan.lee** — 9:22 AM
Are you filtering by `is_current = true`? 
If you just join on `customer_id`, you’re getting every historical subscription change (upgrades, seat additions, etc.) for every customer. 
`fact_subscriptions` is a SCD (Slowly Changing Dimension) style table. 
You need to filter for the specific month-end or just use `is_current` for today's snapshot. 

**carlos.sanchez** — 9:25 AM
Ah, that’s it. I see 15 rows for 'Globex Corp' (CUST-1001) because they keep adding 5 seats every month. 
Wait—if I use `is_current`, how do I get the NRR from 12 months ago? 

**jamie.chen** — 9:30 AM
You can't just use `is_current` for historical. 
Try this: 
`SELECT sum(mrr_usd) FROM nexus-analyst-demo.acme.fact_subscriptions WHERE start_date <= '2025-06-01' AND (end_date > '2025-06-01' OR end_date IS NULL)`
That’ll give you the cohort's starting MRR. 
Then compare it to their MRR in the same bucket for 2026. 
Just make sure you're looking at `nexus-analyst-demo.acme.dim_customers` to filter out the `Free` tier, or your denominator will be huge and your NRR will look like 2%. 

**carlos.sanchez** — 9:45 AM
Okay, that worked. Now I'm getting 118% NRR for the Enterprise segment. 
Does that sound right for 'Stark Industries' (CUST-2020)? They had a massive expansion in March. 

**dan.lee** — 9:48 AM
Yeah, Stark moved from Business to a Custom Enterprise plan. 
They went from $7,500 MRR to $45,000 MRR basically overnight. 
Check `change_type` in `fact_subscriptions`—it should be flagged as `UPGRADE`. 

---

# #coffee-talk — 2026-06-26

**sarah.jenkins** — 10:05 AM
Is the espresso machine in the SF office down again? 
It’s making a sound like a SQL query with 14 nested subqueries. ☕️

**marcus.obrien** — 10:10 AM
I think it’s just the "Workday-to-BigQuery" sync hum. 
Actually, Office Ops said the technician is coming at 2 PM. 
Until then, we’re back to the instant stuff in the back of the pantry. 

**sarah.jenkins** — 10:12 AM
I’d rather drink the leftover water from the dbt-server cooling fans. 

---

# #data-help — 2026-06-27

**marcus.obrien** — 11:30 AM
Quick question on `fact_workflow_runs`. 
I’m seeing a spike in `error_code = 'ERR_429'` for a bunch of SMB accounts this morning. 
Is that a platform issue or are they just hitting their limits? 

**jamie.chen** — 11:45 AM
`ERR_429` is rate-limiting. 
Check `dim_plans.workflow_run_quota_per_month`. 
A lot of the Pro tier folks (10k quota) have been hitting it early because of that new "Auto-Retry" feature Product launched last week. 
If they have a loop in their workflow, they burn through 10,000 runs in about 20 minutes. 

**marcus.obrien** — 11:50 AM
Can we get a list of those customers? 
If they're hitting limits, it's a perfect lead for the AEs to push them to the Business tier. 
I'll run a query on `nexus-analyst-demo.acme.fact_workflow_runs` and join it with `dim_customers`. 

**dan.lee** — 11:55 AM
Use the `mart_daily_utilization` view instead. 
It already aggregates usage vs. quota. 
Save yourself the 4-table join. 
`SELECT company_name, current_plan_tier, run_count, quota FROM nexus-analyst-demo.acme.mart_daily_utilization WHERE pct_usage > 0.9`

**marcus.obrien** — 12:05 PM
Bless you, Dan. You just saved me 30 minutes of debugging why my `run_id` count didn't match the dashboard. 

---

# #ops-status — 2026-06-27

**system** — 1:00 PM
**[INFO]** Scheduled dbt Cloud run `prod_daily_refresh` completed successfully. 
Models updated: 42. 
Rows processed: 1.2M. 
Warehouse: `NEXUS_ANALYST_DEMO`. 

**dan.lee** — 1:05 PM
VRS (Vital Record Sync) looks clean. 
`fact_invoices` matches the Stripe export to the cent. 
Finance can start the month-end close. 

**jamie.chen** — 1:10 PM
Wait, did the `dim_employees` table update? 
I don't see the new hires from the London office in there yet. 
They were supposed to be added to the Amsterdam (EMEA) region. 

**dan.lee** — 1:15 PM
HR hasn't updated the "is_active" flag in the source system. 
It’ll flow through tomorrow once they finish onboarding. 

---

# #random — 2026-06-28

**sarah.jenkins** — 12:30 PM
Who left the half-eaten burrito in the "Data Science" fridge? 
It’s becoming a sentient entity. 
I’m pretty sure it just tried to explain a Random Forest regressor to me. 🌯

**dan.lee** — 12:35 PM
Probably Carlos. He’s been living in the office trying to finalize the Q2 churn forecast. 
He says the model is "drifting." 
The burrito is probably more accurate than the forecast at this point. 

**carlos.sanchez** — 12:40 PM
Hey! I heard that. 
And for the record, the burrito was from yesterday's lunch-and-learn. 
Also, the churn forecast is fine, we just didn't account for 'Initech' (CUST-3030) canceling their 500-seat contract because they "found a guy who could do it cheaper with spreadsheets." 🙄

**marcus.obrien** — 12:45 PM
Classic. Can't wait for them to come back in 6 months when the "spreadsheet guy" quits. 
Add them to the `winback_prospects` list in Salesforce.

# data-help — 2026-06-29

**marcus.obrien** — 9:15 AM
Hey team, trying to calculate NRR for the Board deck. My numbers for the Enterprise cohort are coming out at like 400% which... as much as I’d love to tell the Board that, seems suspicious. 

I’m joining `dim_customers` to `fact_subscriptions`. 

```sql
SELECT 
  sum(mrr_usd) 
FROM nexus-analyst-demo.acme.fact_subscriptions s
JOIN nexus-analyst-demo.acme.dim_customers c ON s.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
AND s.is_current = true
```

What am I missing?

**dan.lee** — 9:22 AM
Marcus, you’re double-counting. `fact_subscriptions` tracks every change (upsells, seat additions, etc). Even with `is_current = true`, if a customer had two concurrent subscriptions (like a base plan + a specialized add-on we used to do in 2024), you might be getting duplicates depending on how you're grouping. 

Also, check your join. `dim_customers` is a flat table, but if you don't filter `status = 'active'`, you're pulling in MRR for churned accounts that might still have a "current" flag hanging around from the last billing cycle. 

Try using `nexus-analyst-demo.acme.mart_daily_utilization` instead if you just need the current MRR snapshot. It’s already cleaned.

**sarah.jenkins** — 9:45 AM
Also Marcus, remember that `Initech` (CUST-3030) and `Massive Dynamic` (CUST-9921) have custom billing schedules. If you look at `fact_subscriptions`, their `mrr_usd` might look inflated because of the way the Series B expansion was booked. 

**marcus.obrien** — 10:02 AM
Got it. The `mart_daily_utilization` table looks much more sane. NRR is sitting at 122% now. Still great, but not "buy a private island" great. Thanks Dan.

---

# #random — 2026-06-30

**carlos.sanchez** — 8:45 AM
PSA: The espresso machine in the SF office is leaking again. Please do not try to "fix" it by jamming a folded post-it note under the water tank. We are a Series B tech company, we can afford a plumber. ☕️

**jamie.chen** — 9:10 AM
@carlos.sanchez I'll put a ticket in with Facilities. In the meantime, the Amsterdam office reports that our coffee machine is working perfectly and the stroopwafels are fresh. Just saying. 🇳🇱

**dan.lee** — 9:12 AM
Don't rub it in, Jamie. Some of us are surviving on burnt beans and 2-hour-old standup notes. 

---

# #data-help — 2026-07-01

**lisa.wong** — 2:30 PM
Quick question on `fact_workflow_runs`. I'm trying to see if there's a correlation between `step_count` and `error_code`. 

Does `error_code = 'NULL'` mean the run was successful, or should I be looking at the `status` column specifically? 

**dan.lee** — 2:35 PM
Always use `status = 'success'`. `error_code` is only populated when `status = 'failed'`. 

Wait, are you querying the raw `fact_workflow_runs` table? That thing is nearly 800 million rows now. You're going to blow the BigQuery budget for the month. 📉

**lisa.wong** — 2:38 PM
Oops. Yeah, I was. It was taking forever to return. 

**dan.lee** — 2:40 PM
Stop! 🛑 
Use the pre-aggregated table: `nexus-analyst-demo.acme.mart_workflow_performance`. 
It has `daily_success_rate` and `avg_step_count` per customer. 

If you absolutely HAVE to use the fact table, make sure you partition by `triggered_at`. 

`SELECT * FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE triggered_at > '2026-06-01'`

Otherwise, Finance is going to come for my head. 

---

# #ops-status — 2026-07-02

**system** — 9:00 AM
**[ALERT]** VRS (Vital Record Sync) failed for `salesforce_accounts` -> `dim_customers`.
Error: `Unexpected schema change in source: field 'last_funding_round' not found.`

**dan.lee** — 9:05 AM
Marcus, did you guys change a field name in Salesforce again without telling us? 

**marcus.obrien** — 9:12 AM
Marketing wanted to track "Liquidity Event" instead of "Funding Round." I didn't think it would break the data warehouse. It’s just a label change? 

**dan.lee** — 9:15 AM
It's never "just a label change" in a relational database, Marcus. 
I have to update the dbt model and the VRS mapping now. 
`dim_customers` will be stale for the next 4 hours. 

**sarah.jenkins** — 9:20 AM
That explains why my Gainsight dashboard is showing 0 MRR for everyone. I was about to have a heart attack. 

---

# #data-help — 2026-07-03

**carlos.sanchez** — 11:00 AM
Does anyone know the logic for `is_active` in `dim_users`?
I'm seeing some users who haven't logged in since 2025 but are still marked as `is_active = true`.

**dan.lee** — 11:05 AM
`is_active` in `dim_users` just means they haven't been de-provisioned by their admin. 
If you want to see if they are *actually* using the platform, you need to join with `dim_users.last_login_date` or check `fact_user_events`. 

We define an "Active User" for North Star metrics as anyone with an event in `fact_user_events` in the last 28 days. 

```sql
SELECT 
  count(distinct user_id) 
FROM nexus-analyst-demo.acme.fact_user_events 
WHERE event_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY)
```

**carlos.sanchez** — 11:10 AM
Ah, got it. I was trying to calculate "Seat Utilization" for the `Hooli` (CUST-1010) account. They are paying for 500 seats but it looks like only 12 people have logged in this month. 

**marcus.obrien** — 11:15 AM
@sarah.jenkins — sounds like a churn risk for the Hooli renewal in Q4. Can you flag that in the CS tracker? 

**sarah.jenkins** — 11:20 AM
On it. I'll reach out to their VP of Ops. They probably just haven't finished the migration from their old tool.

---

# #random — 2026-07-04

**dan.lee** — 10:00 AM
Happy 4th to the US team! 🎆
For those of us in the Amsterdam office... it’s just Thursday. 
I'll be in the warehouse if anyone needs me. 
(Actually, I’m going to go buy more stroopwafels. Don't tell Sarah.)

# #data-help — 2026-07-05

**elena.rossi** — 9:45 AM
Quick sanity check on NRR (Net Revenue Retention). I’m running a report for the board prep and my numbers for Q2 are coming out at 114%, but the automated "Executive Summary" dashboard says 108%. 

Who owns the `calc_mrr_movements` logic?

**dan.lee** — 10:02 AM
That would be me. The dashboard uses the `nexus-analyst-demo.acme.fact_subscriptions` table to calculate the delta between `current_mrr_usd` and the MRR from 12 months ago for the same cohort. 

Are you including the "Expansion" from the `Globex` (CUST-1002) upsell that happened on June 30th? It might not have cleared the `fact_invoices` filter if you’re looking at "Paid" only. 

**elena.rossi** — 10:15 AM
Ah, that’s it. I was looking at `fact_invoices` where `status = 'paid'`. Globex is still 'pending' because of their Net-60 terms. 

But shouldn't NRR reflect the contracted value, not the cash collected? @priya.sharma how did we report this to the VCs last time?

**priya.sharma** — 10:22 AM
We always report on Bookings/Contract Value for NRR. If we waited for Globex to pay their bill, our retention metrics would look like a roller coaster. 

**dan.lee** — 10:30 AM
If you want the contracted NRR, use `fact_subscriptions` and filter for `is_current = true`. Avoid `fact_invoices` for real-time SaaS metrics, it's too laggy because of the Finance team's reconciliation process.

```sql
-- Use this for the "official" MRR snapshot
SELECT 
  sum(mrr_usd) 
FROM nexus-analyst-demo.acme.fact_subscriptions 
WHERE is_current = true 
  AND status = 'active'
```

---

# #random — 2026-07-06

**tom.chen** — 12:15 PM
Is the espresso machine in the SF kitchen leaking again or is that a new "feature"? 

**marcus.obrien** — 12:18 PM
It's a "Liquidity Event" for the drip tray. 

**dan.lee** — 12:20 PM
Lmao. Marcus, stop. 

**sarah.jenkins** — 12:25 PM
I've put a ticket in with Facilities. In the meantime, there’s a cold brew keg in the corner. Just don’t touch the nitro tap, it’s basically a fire hose.

---

# #data-help — 2026-07-08

**tom.chen** — 2:30 PM
I'm trying to find the "Success Rate" of workflows for the `Initech` (CUST-1004) account. They are complaining about "flaky integrations." 

I’m looking at `nexus-analyst-demo.acme.fact_workflow_runs`. What's the difference between `error_code` NULL and `status = 'success'`?

**dan.lee** — 2:45 PM
`status = 'success'` is the definitive flag. 
Sometimes `error_code` is NULL but the status is 'failed' if the runner timed out before it could even throw a specific exception. 

Try this:
```sql
SELECT 
  customer_id,
  count(*) as total_runs,
  sum(case when status = 'success' then 1 else 0 end) / count(*) as success_rate
FROM nexus-analyst-demo.acme.fact_workflow_runs
WHERE customer_id = 'CUST-1004'
  AND triggered_at >= '2026-06-01'
GROUP BY 1
```

**tom.chen** — 2:55 PM
Yikes. Their success rate is 74%. That’s terrible for a "Business" tier customer. 
It looks like most of the errors are `ERR_602_TIMEOUT`. 

**sarah.jenkins** — 3:05 PM
@tom.chen — `Initech` is trying to run 5,000-step loops on a Business plan. They really need to be on the Enterprise tier for the high-concurrency clusters. Can we pull a report of their `step_count` distribution from `fact_workflow_runs`? 

**dan.lee** — 3:10 PM
Yeah, the flat table has `step_count`. I’ll DM you the results. Spoiler: they are way over the standard quota.

---

# #data-help — 2026-07-10

**carlos.sanchez** — 4:00 PM
Does anyone know why `dim_customers.current_mrr_usd` doesn't match the sum of `fact_subscriptions.mrr_usd` for `Aperture Science` (CUST-1022)?

**dan.lee** — 4:15 PM
Check the `billing_cycle`. 
Aperture has two subscriptions: one annual (paid upfront, MRR is `total / 12`) and one monthly "Overage" seat pack. 
The `dim_customers` table is a "FLAT" snapshot and sometimes the sync from Stripe to the warehouse gets weird if there are multiple active subscriptions for one entity. 

Actually... wait. I see the issue. 
Someone manually updated the `seat_count_licensed` in the CRM but didn't update the contract. 

**carlos.sanchez** — 4:20 PM
Is that why the VRS (Value Realization Score) is showing as `-1`?

**dan.lee** — 4:22 PM
Yes. If `seat_count_licensed` is 0 (or null) and they have active events, the VRS formula divides by zero and the model just spits out -1 to avoid breaking the dbt run. 

I'll fix the record for CUST-1022. Please don't tell the auditors the warehouse has a "fix the record" manually step. 

---

# #random — 2026-07-11

**sarah.jenkins** — 9:00 AM
Reminder: The Amsterdam office is closed tomorrow for a local holiday. 
If you ping Dan, he will only respond in stroopwafel emojis. 

**dan.lee** — 9:05 AM
🧇🧇🧇
(Actually I'm still working on the `fact_user_events` partitioning. We’re hitting the 2TB limit on the daily scan and it’s getting expensive.)

# #data-help — 2026-07-12

**carlos.sanchez** — 10:15 AM
Hey data team, I’m trying to calculate Net Revenue Retention (NRR) for the MM (Mid-Market) segment in Q2, but my numbers are coming out way higher than Marcus’s board deck. 
I’m joining `nexus-analyst-demo.acme.dim_customers` to `nexus-analyst-demo.acme.fact_subscriptions` on `customer_id`. 

Is it possible we’re double-counting upgrades? I see some customers with two `is_current = TRUE` rows if they upgraded mid-month. 

**dan.lee** — 10:30 AM
Ah, the "mid-month upgrade ghost." 👻
Yeah, if a customer moves from `Business` to `Enterprise` (like `Globex Corp` did back in April), the `fact_subscriptions` table might show both records as active for a 24-hour window while the prorated invoice clears. 

Filter by `subscription_id` and use the one with the later `start_date`, or just use the `current_mrr_usd` in the `dim_customers` flat table if you just need the "as of now" view. The flat table handles the dedupe logic in the dbt model.

**carlos.sanchez** — 10:35 AM
Got it. Also, why does `Soylent Corp` (CUST-1009) show an MRR of $0 in `fact_subscriptions` for June, but they have 150 active users in `fact_user_events`? 

**sarah.jenkins** — 10:38 AM
@carlos.sanchez Soylent is on a "Bridge" contract. They churned from `Business` but we gave them 90 days of "Free" Enterprise access while their new procurement department settles the legal redlines for the 2027 renewal. 
Status should be `Active` but `plan_tier` is `Free` (Internal-Only tier). 

**dan.lee** — 10:45 AM
Note: If you're running usage queries on `nexus-analyst-demo.acme.fact_workflow_runs` for those guys, the `error_code` might spike because the `Free` tier quota is technically 100 runs/mo, but I think Engineering white-listed their `customer_id` in the infra. 

---

# #random — 2026-07-13

**tom.chen** — 11:45 AM
Does the coffee machine on the 4th floor sound like a jet engine to anyone else? I think it’s about to hit escape velocity. 

**emily.nguyen** — 11:50 AM
It’s been like that since the Amsterdam team visited. I think someone tried to put stroopwafel crumbs in the grinder. 

**dan.lee** — 11:52 AM
🧇🚀 

---

# #data-help — 2026-07-13

**emily.nguyen** — 2:00 PM
Question for the warehouse wizards: I’m looking at `nexus-analyst-demo.acme.dim_users` and trying to find the "Activation Rate" for the new `Pro` tier signups from June. 
Definition of "Active" = at least 3 `workflow_published` events in the first 7 days. 

Where are the event names stored? I don't see them in `fact_user_events`.

**dan.lee** — 2:15 PM
We flattened them. Look for the `event_type` column in `nexus-analyst-demo.acme.fact_user_events`. 
The mapping is:
- `workflow_published` -> `event_type = 'action_dispatch'` with `feature_area = 'builder'`
- `workflow_run` -> go to `fact_workflow_runs` (it's a separate grain because of the volume).

Actually, Emily, check `nexus-analyst-demo.acme.fact_user_events`. I added a `is_core_event` boolean last week that flags the "Golden Actions" (publish, invite, or connection_auth). Use that for activation.

**emily.nguyen** — 2:20 PM
Perfect. Wait, I’m seeing `Hooli` (CUST-1050) has 400 users but only 12 are `is_active = TRUE`. Is that right? 

**sarah.jenkins** — 2:25 PM
@emily.nguyen Yeah, Hooli is a mess. They did a mass-provisioning via Okta but they haven't finished their "Automation Bootcamp." 
I’m meeting with their VP of IT tomorrow to discuss why they’re paying for 500 seats on a `Business` plan but only using a dozen. 
This is going to kill my VRS (Value Realization Score) for the quarter. 

**tom.chen** — 2:30 PM
If they churn, don't look at me. I closed that deal fair and square. 🏃💨

---

# #data-help — 2026-07-14

**carlos.sanchez** — 9:00 AM
Internal Audit is asking for the "Bookings Annualization" report. 
They want to see the delta between `mrr_usd` and the actual `amount_usd` in `fact_invoices` for all `Annual` billing cycles. 

I’m seeing a mismatch for `Wayne Enterprises` (CUST-1033). 
`fact_subscriptions` says MRR is $12,500. 
`fact_invoices` shows a payment of $150,000 in January 2026. 
Math adds up ($12.5k * 12), but the `paid_at` date in the invoice table is missing for the second installment of their seat expansion?

**dan.lee** — 9:15 AM
Wayne Enterprises pays via wire transfer, not Stripe. 
Finance has to manually mark those as `status = 'paid'` in the source system. 
The sync runs at midnight. If they paid yesterday, it won't show up in the `nexus-analyst-demo.acme.fact_invoices` table until tomorrow's partition refresh. 

**carlos.sanchez** — 9:20 AM
Can we get a `dim_payment_methods` table? Distinguishing between `CC`, `Wire`, and `Internal_Credit` would save me a lot of DMs.

**dan.lee** — 9:22 AM
It's on the roadmap for Q4. Right now, I'm just trying to keep the `fact_user_events` table from melting the BQ budget. We just hit 4 billion rows and the `daily_scan_gb` is... spicy. 🌶️

---

# #random — 2026-07-14

**sarah.jenkins** — 12:05 PM
Lunch poll:
🌮 - Tacos (The usual spot)
🍜 - Ramen (It's raining, somehow, in July?)
🥪 - Banh Mi
🥗 - "I am a leaf on the wind" (Salad)

**tom.chen** — 12:10 PM
🌮🌮🌮 (I have a $50 credit because they messed up my order last time)

**dan.lee** — 12:12 PM
🍜 (I need the salt to survive this dbt refactor)

#data-help — 2026-07-15

**carlos.sanchez** — 10:15 AM
Hey @dan.lee, I’m trying to pull the NRR (Net Revenue Retention) for the MM (Mid-Market) segment for the Board Deck. 
I’m joining `nexus-analyst-demo.acme.dim_customers` to `nexus-analyst-demo.acme.fact_subscriptions`, but my numbers are looking way too high. 
Like, 400% NRR high. I wish we were that good, but I think I’m double-counting.

**dan.lee** — 10:18 AM
Are you filtering for `is_current = true`? 
If you just join on `customer_id`, you're getting every historical subscription row for every customer. 
`fact_subscriptions` tracks the full lifecycle—upsells, downsells, seat expansions. 

**carlos.sanchez** — 10:22 AM
Ah, that’s it. I see it now. 
Wait, if I want to see the MRR at the *start* of the period (say, July 2025) vs now, I shouldn’t use `is_current`, right?

**dan.lee** — 10:25 AM
Correct. You’ll need to point-in-time it. 
Use `start_date` and `end_date` to find what was active on 2025-07-01. 
Actually, use the `dim_dates` table to handle the join logic if you want to be safe. 
Also, watch out for `Initech` (CUST-1102). They had a weird mid-month migration from Pro to Business that created two overlapping rows in the `fact` table for about 48 hours. 

**carlos.sanchez** — 10:30 AM
God, I hate manual migrations. 
One more thing: why does `Hooli` (CUST-1089) have a `null` `ae_employee_id` in `dim_customers`? 
They’re paying $12k/mo, someone should definitely be getting commission for that.

**tom.chen** — 10:35 AM
Hooli was a PLG expansion that went sideways. 
They started on Free, someone put it on a corporate card for 200 seats (Pro), and then they upgraded to Business via the "Contact Sales" button but the lead never got routed in Salesforce. 
I’m technically the AE on record now, but Ops hasn't updated the warehouse yet. 
@carlos.sanchez — if you fix that in the report, make sure I get credit for the Q2 kicker. 🤑

---

# #random — 2026-07-15

**sarah.jenkins** — 1:00 PM
Is the espresso machine in the SF office broken again? 
It’s making a sound like a jet engine but no coffee is coming out. 

**tom.chen** — 1:05 PM
It’s "self-cleaning." Which is code for "don't touch it for 20 minutes or it will explode." 
There’s a Blue Bottle run happening in 5 mins if you want in.

---

# #data-help — 2026-07-16

**sarah.jenkins** — 9:45 AM
@dan.lee I’m looking at the `VRS` (Value Realization Score) for the Enterprise cohort. 
I’m seeing a massive dip for `Soylent Corp` (CUST-1055). 
Their score dropped from 85 to 12 overnight. 
Is there a data lag in `fact_workflow_runs`?

**dan.lee** — 10:02 AM
Checking... 
Okay, it's not a lag. The `fact_workflow_runs` table is up to date. 
The issue is their `error_code` count. 
Soylent pushed a change to their internal API yesterday and now every single one of their "Stock Auto-Refill" workflows is throwing a `500` error. 
Since VRS is weighted by *successful* runs (`status = 'success'`), their score cratered.

**sarah.jenkins** — 10:05 AM
Can we set up an Alerting Slack bot for this? 
The CSM (I think it’s @emily.wong) should probably call them before they realize their entire supply chain automation is dead. 

**dan.lee** — 10:10 AM
I can build a view for "High-Error-Volume-Customers" in BQ, but I can't pipe it to Slack without hitting the `workflow_run_quota`. 
Ironically, I’d have to use our own product to send the alert, and my dev account is throttled. 
@carlos.sanchez — can you bump the seat count on the `Internal_Data_Testing` account?

**carlos.sanchez** — 10:12 AM
Only if you help me with the "Bookings vs Billings" reconciliation first. 
Finance is breathing down my neck because `fact_invoices` total for June is $40k lower than the `mrr_usd` sum in `fact_subscriptions`. 

**dan.lee** — 10:15 AM
Check for `status = 'voided'` or `status = 'draft'` in `fact_invoices`. 
We had a bunch of billing errors for the EMEA customers (Amsterdam office) because of the VAT calculation logic change on June 1st. 
A lot of those invoices were thrown out and recreated. 

---

# #ops-announcements — 2026-07-16

**ops-bot** — 12:00 PM
**REMINDER:** Weekly Revenue Standup moved to 2:00 PM PDT today. 
Be prepared to discuss:
- Q3 Pipe Coverage
- The `Business` plan churn at `Cyberdyne Systems`
- Data integrity issues in `dim_customers.account_tier` (Seeing some 'SMB' labels on $100k accounts??)

---

# #data-help — 2026-07-17

**carlos.sanchez** — 2:30 PM
Quick question for anyone who knows the `nexus-analyst-demo.acme.fact_user_events` schema. 
What’s the difference between `event_name = 'workflow_created'` and `event_name = 'template_deployed'`? 
I’m trying to calculate "Time to Value" for the Free tier.

**dan.lee** — 2:45 PM
`workflow_created` is when they start from a blank canvas. 
`template_deployed` is when they use one of the pre-built flows from the Library. 
Usually, `template_deployed` leads to a much higher 7-day retention, but lower long-term stickiness because they never learn how the logic actually works. 
If you’re looking at `fact_user_events`, PLEASE filter by `event_date`. 
If you do a `SELECT *` on that table without a partition filter, I will personally come to your desk and take your laptop away. 
That table is the reason our BigQuery bill is $15k a month. 💸

**carlos.sanchez** — 2:48 PM
Noted. `WHERE event_at >= '2026-07-01'`. 
(And don't worry, I'm using the FLAT version, not the nested one Eng uses).

# #data-help — 2026-07-20

**kim.nguyen** — 9:15 AM
Hey team, I'm trying to pull the NRR (Net Revenue Retention) for the `Business` tier accounts that moved to `Enterprise` last quarter. 
When I join `nexus-analyst-demo.acme.fact_subscriptions` to `dim_customers` on `customer_id`, my totals are coming out way higher than the board deck. 
I think I'm double-counting the months where they upgraded?

**dan.lee** — 9:42 AM
@kim.nguyen You’re probably not filtering for `is_current = true` if you want a point-in-time snapshot, OR you’re not handling the `change_type` correctly. 
If a customer upgraded, they have two records in `fact_subscriptions` for that period—one for the old plan and one for the new one. 
Look at `changed_from_subscription_id` to link the chain. 
Also, check if you're looking at `mrr_usd` or annualizing it. The board deck usually uses ARR (MRR * 12).

**kim.nguyen** — 10:05 AM
Ah, `is_current` was the killer. I was just summing everything. 🤦‍♀️
Quick follow-up: Should I use `account_tier` from `dim_customers` or the `plan_tier` from `fact_subscriptions`? 
I’m seeing some `Business` plan users labeled as `SMB` in the customer dim.

**dan.lee** — 10:12 AM
Use `plan_tier` for revenue math. `account_tier` is a subjective label Sales puts on the account based on their total employee count (SMB/MM/Ent), not what they actually pay us. 
We have a few "SMB" accounts like `Cyberdyne Systems` that are actually on the `Business` tier because they have 60 seats but only 100 total employees. 

---

# #random — 2026-07-21

**sarah.miller** — 8:30 AM
SF Office Update: The espresso machine on the 3rd floor is leaking again. 
Facility team says parts are 2 days out. 
Please use the 4th floor machine or go to the Blue Bottle on the corner (keep your receipts, it's on the "Morale" budget for today). ☕️

**carlos.sanchez** — 8:45 AM
Does the "Morale" budget cover oat milk lattes? Asking for a friend. 

**sarah.miller** — 8:46 AM
Only if that friend closes their Salesforce tasks from Q2. Looking at you, Carlos.

---

# #data-help — 2026-07-22

**carlos.sanchez** — 11:20 AM
Does anyone know the logic for "Active User" in our 2026 KPI dashboard? 
Is it just `last_login_date` in `dim_users` within the last 30 days? 

**dan.lee** — 11:35 AM
No, we moved away from `last_login_date` because it doesn't account for API-only users or people who stay logged in via SSO for months. 
The canonical "Active User" definition is: 
`SELECT DISTINCT user_id FROM nexus-analyst-demo.acme.fact_user_events WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY)`
We use a 28-day window to avoid day-of-week bias. 

**carlos.sanchez** — 11:40 AM
Got it. Does `workflow_run` count as a user event? 
Or is that just the system running a schedule?

**dan.lee** — 11:45 AM
Workflow runs are in `fact_workflow_runs`. If it's a `triggered_by = 'webhook'` or `'schedule'`, it doesn't count toward MAU. 
If it's `triggered_by = 'manual'`, we count it. 
Check the `triggered_by` column in `nexus-analyst-demo.acme.fact_workflow_runs`. 
But honestly, just stick to `fact_user_events` for anything related to "human" engagement.

---

# #ops-announcements — 2026-07-23

**ops-bot** — 09:00 AM
**VRS (Validation & Reporting System) Status Update:**
- `dim_customers`: GREEN (Updated 2h ago)
- `fact_subscriptions`: YELLOW (Latency detected in Stripe sync; MRR for 2026-07-22 might be slightly understated)
- `fact_workflow_runs`: GREEN (6.2M rows processed this morning)

**dan.lee** — 09:15 AM
The Stripe latency is due to a webhook backlog in the Amsterdam region. 
Eng is looking at it, but don't run any "Final" July reports until the status turns Green.

---

# #data-help — 2026-07-24

**kim.nguyen** — 3:05 PM
Need a sanity check on `fact_invoices`. 
I have a customer (`Weyland-Yutani`) who has an invoice for $0 in June, but their `current_plan_tier` is `Business`. 
Is this a trial or a bug?

**carlos.sanchez** — 3:15 PM
Check `fact_subscriptions.change_type`. 
They might have had a service credit from that outage in May. 
CSMs have the authority to issue "One-time Credits" which show up as $0 invoices even if the seat count is high. 
Also, verify the `status` in `nexus-analyst-demo.acme.fact_invoices`. 
If it's `voided`, ignore it.

**kim.nguyen** — 3:22 PM
`change_type` is `credit_adjustment`. That explains it. 
Thanks Carlos! 

---

# #random — 2026-07-25

**dan.lee** — 12:10 PM
Lunch train to the Ramen shop starting in 5 mins. 
Meeting at the SF lobby. 
@carlos.sanchez you coming or are you still fighting with BigQuery?

**carlos.sanchez** — 12:11 PM
I'm one `JOIN` away from either solving this or quitting. 
Go without me, save a seat for my sanity. 🍜

**sarah.miller** — 12:15 PM
Don't forget we have the Q3 Planning kick-off at 1:30 PM. 
If anyone is late because of the ramen line, Marcus will not be happy. 
(Also, does anyone have the updated link for the `Enterprise_Leads` dashboard? The one in the Wiki is 404ing).

**dan.lee** — 12:18 PM
@sarah.miller Data team moved all the "Shadow BI" stuff to the official folder. 
Try: `acme-bi-platform/dashboards/v2/sales-ops-main`
The old one was using the nested tables and it was costing us a fortune in compute. 
The new one uses `nexus-analyst-demo.acme.dim_customers` (FLAT) and it’s like 10x faster.

---

# #data-help — 2026-07-27

**kim.nguyen** — 10:42 AM
Is anyone else seeing weird NRR (Net Retention) numbers for the `Enterprise` cohort in Q2? 
I’m looking at `Globex Corp` and it’s showing 240% retention, which feels... optimistic? 
Even for them.

**carlos.sanchez** — 10:48 AM
@kim.nguyen You’re probably joining `fact_subscriptions` to `dim_customers` without filtering for `is_current = TRUE`. 
If they had a mid-month seat expansion (which they did, they added 150 seats on June 12), you might be summing the old record AND the new record for the same period. 
Check the `subscription_id` logic. 

**kim.nguyen** — 10:55 AM
Ah, yep. I was using the FLAT table `nexus-analyst-demo.acme.fact_subscriptions` but I didn't filter the `change_type`. 
Quick follow-up: Should I be using `mrr_usd` or annualizing it manually from `amount_usd` in the invoices table for the VRS (Volume Report Summary)?

**dan.lee** — 11:02 AM
ALWAYS use `mrr_usd` from `fact_subscriptions` for any official Finance reporting. 
The invoice table includes one-time migration fees and tax, which will bloat your NRR. 
If you need to check seat-based growth specifically, `seat_count` in that same table is the source of truth.

---

# #random — 2026-07-28

**sarah.miller** — 08:30 AM
SF Office: The espresso machine is leaking again. 
Please don't try to "fix" it by jamming a folded napkin under the tray (looking at you, Dan). 
Facilities is coming at 10 AM.

**dan.lee** — 08:32 AM
It wasn't a napkin, it was a high-performance vibration dampener. 
Anyway, I'll be at my desk. 
Reminder: Data Standup is at 09:30 AM. 
We need to discuss the migration of the `fact_user_events` legacy logs. 
Storage costs for `triggered_at` timestamps are getting out of hand.

---

# #data-help — 2026-07-28

**jason.wu** — 01:15 PM
Does anyone know the threshold for `is_active` in `dim_users`? 
I have a user at `Stark Industries` who hasn't logged in since May, but they are still marked as `is_active = TRUE`.

**carlos.sanchez** — 01:20 PM
`is_active` in `dim_users` just means the account isn't deactivated/deleted in our DB. 
It’s a "provisioned" flag, not a "behavioral" flag. 
If you want to see if they are *actually* using the product, you need to join with `nexus-analyst-demo.acme.fact_workflow_runs` and look for `triggered_by = user_id`. 
We usually define "Active Usage" as at least 1 successful workflow run in the last 28 days.

**jason.wu** — 01:25 PM
Got it. So `dim_users.last_login_date` is just for the UI login? 
What if they only run workflows via the API?

**dan.lee** — 01:28 PM
Exactly. A lot of our `Business` and `Enterprise` users never touch the UI after the initial setup. 
They just hit the `/v1/run` endpoint. 
Always rely on `fact_workflow_runs` for engagement metrics. 
The `duration_ms` field is also a good proxy for "complexity" if you're trying to bucket users by sophistication.

---

# #standup-updates — 2026-07-29

**carlos.sanchez** — 09:35 AM
**Daily Data Health Check:**
- `dim_customers`: GREEN (Matches Salesforce sync from 04:00)
- `fact_user_events`: YELLOW (2-hour delay in the event bus ingest for EMEA)
- `fact_invoices`: GREEN

Working on:
- Debugging the `Tyrell Corp` overage calculation. 
They hit their 100k run quota on the `Business` plan but the auto-upgrade didn't trigger. 
AE (Marcus) is asking for the delta.
- Refactoring the `Enterprise_Leads` dashboard to use the new flat schema in `nexus-analyst-demo.acme.dim_customers`. 
The old `region` mapping was broken for APAC.

**sarah.miller** — 09:40 AM
@carlos.sanchez When you look at `Tyrell Corp`, can you also check if they have any `error_code` spikes in `fact_workflow_runs`? 
They’re complaining that their "Nexus-to-Slack" bridge is timing out. 

**carlos.sanchez** — 09:45 AM
Will do. I’ll check the `step_count` too. 
If they have 50+ steps in a single workflow, that might be hitting the execution limit.

---

# #data-help — 2026-07-30

**kim.nguyen** — 04:10 PM
Help! I’m trying to calculate "Average Expansion Time" for the 2025-Q4 cohort. 
I’m looking at `fact_subscriptions` where `change_type = 'expansion'`. 
But some customers have multiple expansion rows in the same month. 
How do I isolate the *first* expansion after their `signup_date` from `dim_customers`?

**dan.lee** — 04:15 PM
Use a window function. 
`RANK() OVER (PARTITION BY customer_id ORDER BY start_date ASC)` 
Filter for rank = 1. 
Make sure you’re looking at `nexus-analyst-demo.acme.fact_subscriptions` (FLAT) and not the raw Stripe tables. 
The raw tables don't handle the `changed_from_subscription_id` mapping correctly for mid-cycle seat adds.

**kim.nguyen** — 04:22 PM
Perfect. Also, does `mrr_usd` in that table account for the `Free` tier? 
I’m seeing $0 for a bunch of rows.

**dan.lee** — 04:24 PM
Yep, `Free` tier is always $0 MRR. 
If you want to filter them out for a "Paying Only" report, just add `WHERE current_plan_tier != 'Free'`. 
Or use `account_tier` if you just want to see the `SMB/MM/Ent` segments. 
Note that `account_tier` is assigned by Sales, whereas `current_plan_tier` is what they are actually being billed for right now.

---

# #random — 2026-07-31

**marcus** — 11:45 AM
End of month push! 
Can someone pull the final July Bookings for the 1:00 PM leadership call? 
I need the split between New Biz and Expansion for the `MM` (Mid-Market) segment.

**dan.lee** — 11:48 AM
@carlos.sanchez is on it. 
Note: The `Weyland-Yutani` credit adjustment we discussed last week is going to show up as a $0 booking for their seat add, so don't be surprised if the Expansion number looks slightly lower than the seat count suggests.

**marcus** — 11:50 AM
As long as the "Logically Active" seats are up, I can explain the revenue gap to the board. 
Thanks for the heads up. 🚀

# #data-help — 2026-08-01

**kim.nguyen** — 09:12 AM
Okay, I’m trying to calculate NRR for the `Ent` segment for July 2026. 
I’m joining `fact_subscriptions` to itself to compare `mrr_usd` this month vs last month, but my numbers are nearly double what the Finance dashboard shows. 
Is it possible I’m double-counting the `changed_from_subscription_id` rows?

**carlos.sanchez** — 09:18 AM
Yeah, you’re definitely double-counting. 
If a customer upgraded mid-month, you’ll have two rows where `is_current` might have been true at different points. 
You need to filter for the *last* record of the month per customer. 
Try: 
`QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id, LAST_DAY(start_date) ORDER BY start_date DESC) = 1`
Also, make sure you're joining on `customer_id` and not just `subscription_id`, because the ID changes on every plan flick.

**kim.nguyen** — 09:25 AM
That helped! But now `Tyrell Corp` is showing up as $0 for June. 
I thought they were a $200k ARR account?

**dan.lee** — 09:28 AM
Check their `status` in `nexus-analyst-demo.acme.dim_customers`. 
They went through a legal restructure in June. Sales paused the subscription for 14 days while the paperwork cleared. 
In `fact_subscriptions`, that shows up as a cancellation and a new start. 
If you’re looking for "Normalized ARR," you might need to bridge that gap manually or use the `v_mrr_bridge` view if the Ops team ever finished it.

**carlos.sanchez** — 09:30 AM
Spoiler: They didn't. Stick to the FLAT tables for now. 
Just a reminder to everyone: `nexus-analyst-demo.acme.fact_subscriptions` (FLAT) is the source of truth for all board decks. 
Don't use the `legacy_` schemas.

---

# #random — 2026-08-01

**marcus** — 12:05 PM
Is the "Taco Tuesday" truck coming today even though it's Wednesday? 
I see a line forming in the parking lot. 🌮

**sarah.jones** — 12:07 PM
They rescheduled because of the rain yesterday! 
Get in line now, `carlos.sanchez` and I are already here. 
The spicy al pastor is calling.

---

# #data-help — 2026-08-03

**sarah.jones** — 10:45 AM
Quick question on the "Vital Resource Score" (VRS). 
Does the `step_count` in `fact_workflow_runs` include internal Acme retries? 
I’m seeing some Enterprise customers with 1M+ steps but only like 500 successful runs.

**dan.lee** — 10:52 AM
`step_count` is the total count of steps executed, regardless of whether the final run status was `success` or `error`. 
If they have a loop in their workflow that's failing, it'll rack up steps. 
For VRS, we usually only care about `status = 'success'`. 
Filter your counts: `count(run_id) where status = 'success'`. 
Otherwise, `Stark Industries` is going to look like our most engaged user when they actually just have a broken webhook hitting a rate limit.

**sarah.jones** — 11:05 AM
Got it. Also, are we still defining "Active User" as `last_login_date` within 28 days? 
Or are we moving to the event-based definition?

**dan.lee** — 11:10 AM
Leadership wants to move to event-based, but the `fact_user_events` table is huge and it's timing out some of the Looker tiles. 
For now, stick to `dim_users.is_active` for high-level reporting. 
If you need the "deep engagement" metric (e.g., users who actually *edited* a workflow), you'll have to query `fact_user_events` and filter for `event_type = 'workflow_edited'`. 
But fair warning: `nexus-analyst-demo.acme.fact_user_events` is partitioned by `event_at`, so use the date filter or the BigQuery bill will make Marcus cry.

---

# #data-help — 2026-08-04

**kim.nguyen** — 02:15 PM
Can someone check the `mrr_usd` for `Initech`? 
I’m seeing a massive spike in the Q3 forecast. 
It looks like they’re being billed for 5,000 seats but their `seat_count_licensed` in `dim_customers` only says 500.

**carlos.sanchez** — 02:22 PM
Checking... 
Ah, I see it. They did a bulk invite yesterday. 
The `fact_subscriptions` table updated because they're on a "Pay-per-seat" Business plan. 
The `dim_customers` table is a daily snapshot—it won't reflect the new `seat_count_licensed` until the overnight ETL run (around 2:00 AM PST). 
If you need real-time seat counts, you have to count the rows in `dim_users` where `customer_id = 'CUST-9923'` and `is_active = true`.

**kim.nguyen** — 02:25 PM
Wait, if they're on the Business plan, isn't there a 50-seat minimum? 
I’m seeing some customers in the `MM` segment with only 10 seats in `fact_subscriptions`. 

**dan.lee** — 02:28 PM
Legacy accounts. We let some early adopters stay on Business even if they dropped below the seat floor. 
Check `signup_date`. If it’s 2023 or early 2024, they're probably grandfathered in. 
Use `account_tier` if you want to group them by how Sales treats them, but `current_plan_tier` if you want to know which features they have access to.

---

# #random — 2026-08-05

**marcus** — 09:00 AM
Morning all! Remainder that the Amsterdam team is on a local holiday tomorrow. 
If you need anything from EMEA Sales, get your pings in today. 🇳🇱

**carlos.sanchez** — 09:05 AM
Does that mean `dim_employees` will show them as `is_active = false`? 😂

**marcus** — 09:06 AM
Don't give the HR team ideas, Carlos. 
Anyway, back to the grind. July numbers look solid. Let's keep the momentum! 📈

---

# #data-help — 2026-08-06

**sarah.jenkins** — 10:14 AM
Hey team, I'm trying to calculate NRR for the July cohort and I'm getting some wild numbers (like 215%). 
I'm joining `dim_customers` to `fact_subscriptions`. 
Is it possible we have duplicate records for the same `customer_id` in the subscriptions table? 

**dan.lee** — 10:18 AM
@sarah.jenkins `fact_subscriptions` isn't a unique list of customers. It’s a history of every plan change, expansion, and contraction. 
If a customer upgraded from Pro to Business mid-month, they'll have two rows for that period. 
You need to filter for `is_current = true` if you want the "right now" state, or join on a specific date range where `start_date <= analysis_date` and `end_date > analysis_date`. 

**carlos.sanchez** — 10:20 AM
Also check the `change_type`. 
If you’re seeing 200%+ NRR, you might be double-counting the `mrr_usd` from both the `changed_from_subscription_id` and the new `subscription_id` in the same join. 
The canonical way to do NRR is in the `nexus-analyst-demo.acme.fact_subscriptions` table using the `mrr_usd` field, but you HAVE to handle the date overlaps. 

**sarah.jenkins** — 10:25 AM
That makes sense. I was just doing a sum on `mrr_usd` grouped by `customer_id`. 🤦‍♀️
I'll add the `is_current` flag. 
Wait, if I use `is_current`, will that exclude churned customers? 

**dan.lee** — 10:28 AM
Yes. Churned customers won't have an `is_current = true` record for today. 
To get NRR, you need to compare the `mrr_usd` from `fact_subscriptions` on 2026-07-01 vs 2026-07-31 for the same set of `customer_id`s. 
Basically, a self-join on the table with two different date filters.

---

# #random — 2026-08-06

**marcus** — 11:45 AM
SF Office: The espresso machine is leaking again. ☕️🚫
Please don't try to "fix" it by jamming a paperclip in the steam wand (looking at you, Engineering). 
I've called the technician. Use the pour-over station in the meantime.

**carlos.sanchez** — 11:48 AM
Can we query the `fact_coffee_consumption` table to see if it's over capacity? 

**marcus** — 11:50 AM
Error 404: Caffeine not found.

---

# #data-help — 2026-08-07

**kim.nguyen** — 09:12 AM
Does anyone know why `fact_workflow_runs` has a bunch of `null` values for `triggered_by`? 
I’m trying to see which users are the most active, but about 40% of the runs don’t have a `user_id` attached.

**dan.lee** — 09:15 AM
Those are likely scheduled jobs or webhook triggers. 
If a workflow is set to run every hour on a cron schedule, there’s no "user" physically clicking a button, so `triggered_by` stays null. 
If you want to attribute that activity to a person, you should join back to the `workflows` table (wait, we haven't flattened that yet—it’s in the `work_in_progress` schema) to see who the `owner_id` is.

**carlos.sanchez** — 09:18 AM
Actually, Kim, if you want "active users" for the Board deck, don't use `fact_workflow_runs`. 
Some users log in just to check the audit logs or change permissions in `fact_user_events`. 
The "Product Active User" (PAU) definition we agreed on is: 
`count(distinct user_id)` in `nexus-analyst-demo.acme.fact_user_events` where `event_at >= date_add(current_date(), interval -28 day)`.
Check the `event_type` list in the internal wiki—we exclude `email_received` because it’s passive.

**kim.nguyen** — 09:22 AM
Got it. So `fact_workflow_runs` is for platform load/scaling metrics, `fact_user_events` is for engagement. 
What about the `status` column in `fact_workflow_runs`? 
I see `error_code` for some, but others are just `failed`. 

**dan.lee** — 09:25 AM
`error_code` is only populated if the underlying SaaS tool (like Salesforce or Slack) returned a specific API error. 
If the workflow timed out on our side, it just says `status = 'failed'` and `error_code` is null. 
Check `duration_ms`—if it's exactly 300,000, it’s a timeout.

---

# #data-help — 2026-08-07

**marcus** — 02:00 PM
Quick check—are we annualizing Bookings based on `amount_usd` in `fact_invoices`? 
Finance is saying my Q3 projected ARR is too high. 

**carlos.sanchez** — 02:05 PM
@marcus don't use `fact_invoices` for ARR! 
Invoices include one-time implementation fees (the $5k "Jumpstart" package) and tax. 
If you annualize that, you're overcounting. 
Always use `mrr_usd` from `nexus-analyst-demo.acme.fact_subscriptions`. 
That table represents the contracted recurring value. 
Multiply the `sum(mrr_usd)` by 12 to get your ARR.

**marcus** — 02:08 PM
Ah, okay. That explains why `Initech` looked so huge last month—they paid their annual Enterprise bill up front plus a $10k migration fee. 
So `fact_invoices` showed $60k but their MRR is actually $4,166. 

**dan.lee** — 02:10 PM
Exactly. `fact_invoices` is for cash flow, `fact_subscriptions` is for growth metrics. 
Also, make sure you're looking at `status = 'paid'` or `status = 'open'` in invoices if you’re doing collections tracking. 
We still have about $40k in "voided" invoices from those trial accounts that never converted.

---

# #random — 2026-08-08

**kim.nguyen** — 08:30 AM
Is it just me or is the Amsterdam standup getting earlier? 🥱

**dan.lee** — 08:32 AM
EMEA started their summer hours. They're trying to wrap by 4 PM CET to head to the canals. 
Good for them, terrible for my sleep schedule. 

**carlos.sanchez** — 08:35 AM
Wait, if they're out, who's approving my PR for the `dim_employees` update? 
I need to mark the new interns as active so they can get into the BigQuery sandbox. 

**marcus** — 08:40 AM
I can ping the Amsterdam lead on WhatsApp. 
But honestly, just tag the `data-eng` on-call. 
I think it's Sarah this week.