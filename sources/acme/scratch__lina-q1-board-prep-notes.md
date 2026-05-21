---
title: "Scratch — Lina's Q1 board prep WIP queries (do not read for correctness)"
source_url: "internal://acme/scratch/lina-q1-prep"
license: "synthetic-demo"
attribution: "Synthetic scratch notebook. Acme Inc internal demo. WIP / WIP / WIP."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# scratch — Lina's Q1 board prep notes

> **WARNING**: this is my personal scratch notebook for Q1 board prep. Some queries are wrong. Some are right. I'm leaving the wrong ones with strikethrough so I remember NOT to use them. If you're reading this, the canonical Q1 numbers are in the board deck (https://drive.google.com/...). NOT here. -lina

## TODO list (working through these for the deck)

- [x] ARR snapshot ✓ (uses `dbt/models/marts/finance/arr_snapshot.sql`)
- [x] NRR trailing 12 ✓ (lock the cohort definition footnote — sam asked)
- [x] Logo growth Q1 (62 new, 15 churned, +47 net)
- [x] Engaged customer rate
- [x] Expansion MRR breakdown
- [x] GRR (added per board ask)
- [ ] cash burn — separate slide, not my deck
- [ ] runway — also not me

## Queries (chronological, not organized)

### Initial NRR pull (got the right answer first try) ✓

```sql
-- Trailing 12mo NRR using the dbt model
SELECT * FROM `nexus-analyst-demo.acme.dbt_marts.nrr_trailing_12`
ORDER BY snapshot_date DESC LIMIT 1;
```

Result: 1.07. ✓ matches what I told sam last quarter.

### ~~First attempt at logo churn breakdown by plan~~ (wrong)

```sql
-- ~~SELECT current_plan_tier, COUNT(*) FROM dim_customers WHERE status = 'churned' GROUP BY 1;~~
-- WAIT this counts current_plan_tier which is set to Free at churn. Useless.
-- Need to look at the plan they were on PRE-churn. 🤦
```

### Logo churn by pre-churn plan ✓

```sql
WITH pre_churn AS (
  SELECT
    s.customer_id,
    s.plan_tier AS pre_churn_plan
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  WHERE s.change_type = 'churn'
)
SELECT
  pc.pre_churn_plan,
  COUNT(*) AS churned_count
FROM pre_churn pc
JOIN `nexus-analyst-demo.acme.fact_subscriptions` prev
  -- WAIT this is broken too, need to join to the changed_from sub for the actual pre-churn plan
GROUP BY 1;
```

Hmm. Fix:

```sql
SELECT
  prev.plan_tier AS pre_churn_plan,
  COUNT(*) AS churned_count,
  SUM(prev.mrr_usd) AS total_pre_churn_mrr
FROM `nexus-analyst-demo.acme.fact_subscriptions` curr
JOIN `nexus-analyst-demo.acme.fact_subscriptions` prev
  ON curr.changed_from_subscription_id = prev.subscription_id
WHERE curr.change_type = 'churn'
  AND curr.start_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY 1
ORDER BY 1;
```

✓ that works. Result for Q1 2026:
- Pro: 9 churns, $4,420 pre-churn MRR ($53K ARR loss)
- Business: 5 churns, $54,000 pre-churn MRR ($648K ARR loss)
- Enterprise: 1 churn, $9,685 pre-churn MRR ($116K ARR loss — that was Beacon)
- Total: 15 churns, $68K MRR ($817K ARR)

> wait that's bigger than I thought. Let me double-check by summing churn from MRR movement model...

```sql
SELECT SUM(churned_mrr_loss_usd) FROM `nexus-analyst-demo.acme.dbt_marts.nrr_trailing_12`
WHERE snapshot_date = '2026-04-30';
```

That's the trailing 12 churn loss not Q1 specific. OK different number. Fine.

For the deck I'll use $817K Q1 ARR churn loss. Cross-check with rachel before locking.

### Random "is engagement actually predictive of retention" sanity check

```sql
-- For customers who churned in Q1 2026, what was their engagement state 30d before churn?
WITH q1_churns AS (
  SELECT customer_id, start_date AS churn_date
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE change_type = 'churn'
    AND start_date BETWEEN '2026-01-01' AND '2026-03-31'
),
engagement_pre_churn AS (
  SELECT
    qc.customer_id,
    COUNT(DISTINCT IF(ev.event_at BETWEEN TIMESTAMP_SUB(TIMESTAMP(qc.churn_date), INTERVAL 30 DAY)
                       AND TIMESTAMP(qc.churn_date), ev.user_id, NULL)) AS active_users_30d_pre_churn
  FROM q1_churns qc
  LEFT JOIN `nexus-analyst-demo.acme.fact_user_events` ev
    ON ev.customer_id = qc.customer_id
    AND ev.event_name = 'login'
  GROUP BY qc.customer_id
)
SELECT
  CASE
    WHEN active_users_30d_pre_churn = 0 THEN '0 (ghost)'
    WHEN active_users_30d_pre_churn < 3 THEN '1-2 (low)'
    WHEN active_users_30d_pre_churn < 10 THEN '3-9 (medium)'
    ELSE '10+ (high)'
  END AS engagement_band,
  COUNT(*) AS n_churns
FROM engagement_pre_churn
GROUP BY 1
ORDER BY 1;
```

Result:
- 0 (ghost): 4
- 1-2 (low): 5
- 3-9 (medium): 4
- 10+ (high): 2

So 9 of 15 (60%) Q1 churns were "low or no engagement" 30d pre-churn. The 2 high-engagement churns were both procurement-driven (Beacon + one I forget — check CRM).

Useful data point. Going to mention in the deck as supporting evidence for why we invest in CSM time on at-risk accounts. Need to confirm with elena before quoting.

## Random other notes

- need to ask david.kim if we can backfill `dim_customers.churn_date` for the 3 customers from Q4 2025 where it's NULL even though they churned. annoying gap in dim hygiene.
- the multi-touch attribution model isn't going to ship in time for this deck. using first-touch for channel mix slide. fine.
- jasmine wants to add a "best-performing campaign by ROAS" slide. waiting on her to send me the spend data overlay.

## Open questions to resolve before lock

1. Should we report GRR alongside NRR? sam said yes, lina (me) is doing it.
2. Should we caveat the engagement-vs-retention slide with "this is correlation not causation"? probably.
3. Marcus wants the AE quota attainment slide split by SMB / MM / Ent. need to pull.

## Lock by Thursday EOD. Deck owner: rachel. Deck location: shared drive.
