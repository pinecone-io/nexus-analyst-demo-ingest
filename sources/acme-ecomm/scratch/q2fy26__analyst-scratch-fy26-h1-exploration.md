---
title: "Analyst scratch notes: H1FY26 exploratory data pulls"
source_url: "internal://acme-ecomm/scratch/q2fy26__analyst-scratch-fy26-h1-exploration"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: confluence_page
---

# Draft Scratch Pad — H1FY26 Exploratory Data Pulls & Pre-MBR Checks
*Author: amara.shah (Data Analyst, Finance/MBR, assoc_100211)*
*Status: Personal Working Draft / Not for external circulation*
*Created: ~2025-07-15 (Mid-Q2FY26 working notes)*

---

### 0. Housekeeping & Standup Notes (Ignore if just looking for numbers)
- Got my desk moved near the water cooler on 3 West. The hum from the vending machine is driving me nuts. 
- Reminder: need to expense the parking validation from last Tuesday's late-night session when carlos.figueroa locked us in the war room preparing for the Q2 check-in. Ever since Carlos got bumped up to VP Data & Analytics back in March (congrats again, carlos.figueroa!), the cadence on these deck prep loops has been relentless.
- Coffee machine on floor 2 is out of oat milk again. 
- Looker-to-Compass dashboard migration is dragging. Some of the legacy tiles are still caching old queries, so always double-check against BigQuery direct pulls if numbers look weird. Remember the flat dataset rule: `nexus-analyst-demo.acme_ecomm.<table>` (no nested paths like `acme_ecomm.marts.*` — remember when that broke the `member_cltv` pulls back in March?).

---

### 1. Quick SQL snippet: Checking H1FY26 traffic vs orders baseline
Just pulling some raw cuts across the 3 core markets (US, CA, MX) to see how conversion is tracking across Q1FY26 and Q2FY26 QTD. 

```sql
SELECT
  date_trunc(date, month) as fiscal_month,
  market,
  vertical_code,
  sum(sessions) as total_sessions,
  sum(orders) as total_orders,
  safe_divide(sum(orders), sum(sessions)) as blended_conversion_rate,
  sum(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-02-01'
  AND date <= '2025-07-15'
GROUP BY 1, 2, 3
ORDER BY 1, 2;
```

*Wait, check this:* when I query `fact_orders` directly for total order counts vs. `fact_traffic_daily`, they don't match up if you aren't careful. 
*Note to self:* `fact_orders` is only a **~400,000-row representative sample**, *not* the population! I almost sent a Slack to wei.hartono yesterday claiming US conversion crashed because I did a `COUNT(*)` on `fact_orders` for a weekly slice. Good thing I checked the schema docs. For actual totals, stick to `fact_traffic_daily` or the aggregate marts (`traffic_conversion_summary`, etc.). Do not use panel tables for company-level aggregates!

---

### 2. Exploring Marketplace sub-verticals (Style vs Resold vs Collectibles)
Victor Okonkwo's team (victor.okonkwo) wants a clean breakdown of how the 3 Marketplace sub-verticals are behaving through Q1 and early Q2. Let's look at the `marketplace_gmv_summary` mart (which *is* full population, thankfully).

Let's write out the query to check Q1FY26 through Q2FY26 QTD:
```sql
SELECT
  fiscal_week_ending,
  sub_vertical_code,
  sum(gmv_usd) as gmv,
  sum(orders) as orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-02-01' AND '2025-07-15'
GROUP BY 1, 2;
```
*Quick eyeball of the numbers from the summary tables:*
- Style: Q1FY26 was $512.0M, Q2FY26 is pacing nicely around $530.0M.
- Resold: Q1FY26 was $88.0M, moving to $97.0M in Q2FY26. Loop Resale Collective (`sel_500204`) is carrying a huge chunk of this growth—they crossed $1M trailing-90d GMV back in May.
- Collectibles: Q1FY26 was $22.0M, Q2FY26 at $25.0M. Still small, but keeping an eye on it. (Wonder if we'll see any weird volatility here later in the year—lucia.ferreira and sanjay.bhatt are keeping close tabs on listing quality).

Let's cross-reference with the seller panel (`dim_seller`). Total active panel size is hovering around 2,050 to 2,200 sellers depending on the week. 
Wait, let me pull a quick distribution check on seller status:
```sql
SELECT
  category_focus,
  status,
  count(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```
Looks clean. The sample has a good mix across our cast elements like `sel_500200` (Silverline Card Co.) and `sel_500203` (Marrow Lane Vintage). 

---

### 3. Care & VOC sanity checks (Medallia baseline)
Giulia Romano (`giulia.romano`) asked me to verify if the Medallia VOC baseline from the July 10 data drop (`fact_voc_responses`) matches what we are seeing in Care contact volumes (`fact_care_contacts`).
- Q1FY26 total contacts: ~2,150K
- Q2FY26 contacts (partial): hovering steady around ~2,205K quarterly run rate.
- Deflection rate is sitting right around 37.2% in Q1 and creeping up to 39.5% in Q2. 
- Medallia refund-delay verbatim share is locked at a very stable **3.5% baseline** right now (per giulia.romano's July 10 drop). No weird spikes. Everything looks super quiet on the customer care front. (Good! Let's hope it stays that way through the rest of Q2).

---

### 4. Membership (Acme+) quick pull
Checking `dim_member` panel (120,000 representative rows) to test out the CLTV mart script before wei.hartono pushes it to production.
Remember the join trap! If I use an `INNER JOIN` between `dim_member` and `fact_orders`, I drop all the dormant members who haven't ordered in the trailing 12 months. 
- *Correct way:* `LEFT JOIN fact_orders ... COALESCE(trailing_12mo_gmv_usd, 0)`
- If you inner join, average CLTV looks like ~$625. If you do it right, it's closer to ~$500 because of the ~20% dormant segment (members like `mem_1000178` "Marisol" who are paying annual dues but have zero recent orders). Must make sure the MBR deck uses the correct table so we don't accidentally overstate member value by 25%!

Let's check Acme+ true base numbers for the board deck:
- Q1FY26 ending base: 12.60M members.
- Q2FY26 (pacing): ~12.90M members (net adds around +300K).
- Annual renewal rate: holding strong at 86.2% in Q1, 86.4% in Q2. 
- Streaming perk (Vidora partnership, launched back on 2025-06-01 by renee.kowalski) is getting good early engagement among multi-benefit adopters, though awareness is still something derek.holloway and renee.kowalski are planning to workshop in Q3.

---

### 5. TODOs / Come back to this on Thursday
- [ ] Check why the Canada conversion rate query is returning nulls for a few rows in late June. Might be a timezone shift in `fact_traffic_daily` for Pacific vs Eastern timestamps.
- [ ] Finish formatting the H1FY26 summary tables for the upcoming leadership sync (the one carlos.figueroa set up for next week).
- [ ] Follow up with nadia.esposito on whether the Aitable to Jira roadmap migration is going to impact our vertical tag mappings in `dim_experiment`.
- [ ] Grab lunch with amara.shah—wait, that's me. Grab lunch with wei.hartono.

---
