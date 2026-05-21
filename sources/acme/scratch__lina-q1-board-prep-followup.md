---
title: "Scratch — @lina.cho Q1 board prep follow-up notes"
source_url: "internal://acme/scratch/lina-q1-board-prep-followup"
license: "synthetic-demo"
attribution: "Acme Inc internal FP&A scratchpad (synthetic demo). Author: Lina Cho."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: scratch_note
---

# Q1 Board Prep Follow-up — @lina.cho

Working notes for the final Q1 2026 board deck. Need to lock these figures by EOD Friday for @rachel.stein's review.

## 1. Attribution Inconsistency (The @jorge.martinez / Salesforce gap)
Still seeing a ~$140K delta between `marts/sales/bookings_attribution.sql` and the raw Salesforce "Bookings by Channel" report for Q1. 
- **The Issue**: It looks like the fix from `postmortem__salesforce-attribution-mismatch-2025-11-30.md` didn't fully account for multi-opp accounts where the `first_touch_at` is being pulled from the *very first* touch across the whole customer history, even if that touch was for a lead that was closed-lost 2 years ago.
- **Action**: @jorge.martinez — can we refine the `first_touch` CTE in `dbt__model__bookings_attribution.md` to look for the first touch *within the 6 months prior* to the opportunity creation date? 
- **Status**: Jorge is looking at the ARRAY_AGG logic. If we can't fix the SQL by Thursday, I'm going to manually override the "Partner" channel total in the deck to match the CRM source-of-truth.

## 2. Gross Margin Assumption
@rachel.stein flagged the COGS spike in March. It’s mostly Snowflake and Datadog overages from the high-volume workflow runs in the Business tier.
- **Reference**: See the thread in `slack__board-prep__gross-margin-question.md`.
- **Assumption**: We are sticking with 78% GM for the Q1 slide. I've verified that the Datadog spike was a one-time indexing error on the `fact_workflow_runs` logging side (thanks @david.kim for the catch).
- **To-do**: Update the "Margin Trends" slide to include a footnote about the March infra anomaly so the board doesn't think our unit economics are degrading.

## 3. NRR Restatement (The "Gnarly" Footnote)
We have to be transparent about the NRR dip in the restated 2025-Q3 figures.
- **The Bug**: As documented in `postmortem__nrr-calculation-bug-2026-03-04.md`, we were using a strict `<` instead of `<=` on the cohort boundary. 
- **The Impact**: NRR for Q3 was reported as 1.09; the corrected figure is 1.07. 
- **Drafting the footnote**: 
  > "*Note: 2025-Q3 NRR has been restated from 1.09 to 1.07 following a correction in the cohort boundary logic. The adjustment reflects the inclusion of customers whose anniversary date fell exactly on the period start boundary. See `dbt__model__nrr_trailing_12.md` for current methodology.*"
- **Check**: @dan.lee — does this wording pass the "product-led growth" sniff test? I don't want it to sound like we're hiding a churn spike.

## 4. Enterprise Expansion vs. Initial Booking
The board is asking for the "Land and Expand" velocity. 
- Using `post_close_mrr_delta_vs_initial_usd` from `dbt__model__bookings_attribution.md`.
- **Finding**: Accounts landed in 2025-H1 on the Business tier are expanding by an average of 14% within the first 6 months. 
- **Highlight**: `cust_000412` (Drag Industries) is the outlier here—they expanded from 30 seats to 85 seats in just 4 months. Need to make sure @marcus.webb has the Gong transcript (`gong__discovery__cust000412-drag-industries.md`) ready if they ask for the qualitative "why."

## 5. Misc / Cleanup
- [ ] Check `dim_plans` for the Pro price change ($49 -> $59). Does the ARR forecast for H2 reflect the new price for new logos?
- [ ] Ping @elena.volkov for the "Top 5 At-Risk" list. I need to make sure none of them are in the "Commit" bucket for the renewal forecast.
- [ ] Verify `arr_usd` in `dbt__model__arr_snapshot.md` matches the Stripe dashboard exactly for the 2026-03-31 snapshot. (Usually off by <$100 due to mid-day churns).

---
*Last updated: 2026-04-28 by @lina.cho*
