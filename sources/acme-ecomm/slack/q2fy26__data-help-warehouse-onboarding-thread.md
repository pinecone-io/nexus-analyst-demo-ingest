---
title: "Slack #data-help thread: new-analyst onboarding on the acme_ecomm warehouse"
source_url: "internal://acme-ecomm/slack/q2fy26__data-help-warehouse-onboarding-thread"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: slack_thread
---

**Channel:** `#data-help`
**Topic:** New analyst onboarding, schema questions, and dataset conventions on the BigQuery `acme_ecomm` data warehouse.
**Date:** July 15, 2025 (Q2FY26)

---

**[2025-07-15 09:14 AM] lexi.vance (Data Analyst - New Hire):**
Hey team! Quick question as I’m getting my bearings in the BigQuery warehouse today. I was trying to pull some initial numbers for a Q2 ad-hoc request and I think I might be hitting a permission or path error. 

When I run a query against `acme_ecomm.marts.membership.member_cltv`, BigQuery is telling me `Not found: Dataset nexus-analyst-demo:acme_ecomm.marts` or something similar. Is there a different permissions group I need to request in Okta for the marts subfolders, or am I looking at the wrong path? 

*(Attaching query snippet)*
```sql
SELECT * 
FROM `nexus-analyst-demo.acme_ecomm.marts.membership.member_cltv` 
LIMIT 10;
```

**[2025-07-15 09:22 AM] connor.blake (Data Engineer):**
Ah, classic trap! Welcome aboard Lexi. 

It’s actually not an Okta permission issue. Remember back when carlos.figueroa and amara.shah pushed through that schema standardization fix around March (following the FY26 kickoff alignment)? The BigQuery dataset is completely **FLAT**. 

Every single table—whether it's a base fact, a dimension, or a derived mart—lives directly under `nexus-analyst-demo.acme_ecomm.<table>`. There are no nested datasets like `acme_ecomm.marts.*` or `acme_ecomm.membership.*`. 

So for that CLTV table, you just want:
```sql
SELECT * 
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` 
LIMIT 10;
```
Give that a spin and let us know if it clears up.

**[2025-07-15 09:25 AM] lexi.vance:**
Oh, amazing! That worked instantly. Thank you, connor.blake! 

While I have you both, I was also looking at the table definitions in our internal documentation for joining `dim_member` to `fact_orders`. Are there any specific join traps I should watch out for when calculating things like trailing orders or CLTV? I want to make sure I don't accidentally drop cohorts.

**[2025-07-15 09:31 AM] wei.hartono (Analytics Engineer):**
Morning Lexi! Jumping in here. 

Yes, watch your joins like a hawk on the panel tables. Remember convention 5: tables like `dim_member`, `dim_seller`, and `fact_orders` are **representative panels/samples**, not full population totals. 

Specifically for `member_cltv`, the canonical build requires a **LEFT JOIN** from `dim_member` to `fact_orders` combined with a `COALESCE(trailing_12mo_gmv_usd, 0)`. If you use an inner join, you'll silently drop about 20% of our 120,000-member panel—the folks who are still active and paying their annual or monthly fees, but happen to have zero orders in the trailing 12 months (like our classic dormant archetype, Marisol). Doing an inner join will artificially inflate your average CLTV by roughly 25% because it weeds out all the zero-spend active members. 

Always check your row counts against the known panel sizes before you sign off on a report!

**[2025-07-15 09:35 AM] lexi.vance:**
That is super important, thank you wei.hartono. I would have definitely defaulted to an inner join for a clean lookup. 

Quick side question: where do our fiscal quarter boundaries live? I'm pulling some date ranges for the rest of Q2FY26 and I want to make sure I'm filtering correctly against our retail calendar (since we start FY on Feb 1). Should I be writing custom date case statements, or is there a standard dimension table for that?

**[2025-07-15 09:40 AM] connor.blake:**
Please, for the love of all that is holy, do *not* write custom date case statements for fiscal quarters. 

We have `dim_date` fully populated for all 761 rows covering the 2025 through 2027 window. It has explicit columns like `fiscal_year`, `fiscal_quarter` (INT64), `fiscal_quarter_label` (e.g., `'Q1FY26'`, `'Q2FY26'`), `fiscal_week`, and `is_peak_holiday`. Just join your fact tables against `dim_date` on `date = date` and pull `fiscal_quarter_label`. 

Since we're currently sitting in Q2FY26 (mid-July 2025, running through July 31), just keep in mind that any incomplete quarter needs a QTD caveat, though Q2 is ticking along nicely since the Medallia VOC baseline checks we ran back in early July locked in our stable ~3.5% refund-delay verbatim baseline.

**[2025-07-15 09:42 AM] lexi.vance:**
`dim_date` it is! Thanks, Connor. I'll make sure to bookmark that table. 

By the way, are we still doing that team coffee chat over by the third-floor micro-kitchen at 10, or did that get pushed?

**[2025-07-15 09:43 AM] connor.blake:**
Still on! Though fair warning, someone brought in those weird gluten-free carob rice cakes again instead of the good peanut butter pretzels, so temper your expectations. 

**[2025-07-15 09:44 AM] wei.hartono:**
Carob rice cakes should be a compliance violation in `acme_ecomm`. 

Anyway Lexi, to reiterate just to make sure it's burned into your muscle memory for retrieval redundancy later:
1. **The dataset is completely flat.** Query `nexus-analyst-demo.acme_ecomm.<table>` directly. No `marts` folders, no nested sub-datasets. 
2. **Panel vs. Population matters.** Aggregate fact tables (`fact_traffic_daily`, `fact_promise_vs_actual`) are full population, but entity/event-grain tables (`dim_member`, `dim_seller`, `fact_orders`, `fact_care_contacts`, `fact_voc_responses`, `fact_marketplace_listings`, `fact_membership_events`) are representative panels. Never run raw `COUNT(*)` or `SUM()` on a panel table expecting company-wide totals (like total company GMV or total active members). Always pull total counts from the aggregate marts or the official MBR/Company figures.
3. **Date boundaries.** Always use `dim_date` for retail fiscal calendar queries (FY starts Feb 1). 

You'll do great. Ping us here if anything else breaks!

**[2025-07-15 09:46 AM] lexi.vance:**
Got it all bookmarked and saved in my local notes. Thanks so much, both of you! Heading down to check if there are any real snacks left before the coffee chat.

---
