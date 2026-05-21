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
