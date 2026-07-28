# ACME (eCOMMERCE) CANON — authoritative fact sheet for source authoring

You are writing ONE synthetic internal source file for "Acme" — a fictitious large
omnichannel retailer + marketplace (in code/config: `acme-ecomm` / BigQuery dataset
`acme_ecomm`). This is a **different fictional company** from "Acme Inc" (the B2B SaaS
in `datasets/acme/CANON.md`) — different industry, different people, different IDs,
different BigQuery dataset, never queried together. Everything below is CANON. Never
contradict it. Bury the SIGNALS (correct facts) inside heavy, realistic NOISE. Reuse
the shared CAST so every file references the SAME entities with the SAME attributes.
This is synthetic demo data (disclaimer in every frontmatter).

**Hard rule — cast disjointness.** Never reuse any person name, handle, customer/
member/seller name, or ID from `datasets/acme/CANON.md` (the SaaS Acme Inc). See
DO-NOT-REUSE below for the explicit forbidden list. If in doubt, invent something new.

---

## Company

- Large US-based omnichannel retailer + marketplace: physical stores, eCommerce, and
  a 3rd-party marketplace, across US / Canada / Mexico. This warehouse models the
  **digital commerce + marketplace + membership** side of the business (the part
  these questions live in) — not in-store POS, which lives in a separate Hive-native
  system out of scope here.
- 16 internal verticals (the taxonomy below). **Deep narrative in 5**: US Conversion +
  Traffic, Marketplace, Care, Speed (fulfillment), Membership. The other 11 are metric
  rows + light mentions only — enough that a cross-vertical query returns something
  real, never enough to carry a storyline.
- **Fiscal calendar**: FY runs Feb 1 → Jan 31 (retail convention). Quarters: Q1
  Feb–Apr, Q2 May–Jul, Q3 Aug–Oct, Q4 Nov–Jan (Q4 is the peak/holiday quarter — Black
  Friday/Cyber Monday + December). For this dataset, quarters are approximated to
  calendar-month boundaries; the real 4-4-5 fiscal-week convention is flavor, not
  load-bearing for any number below.
- **6 modeled quarters**: Q1FY26 (2025-02-01–2025-04-30) · Q2FY26 (2025-05-01–2025-07-31)
  · Q3FY26 (2025-08-01–2025-10-31) · Q4FY26 (2025-11-01–2026-01-31, peak) · Q1FY27
  (2026-02-01–2026-04-30) · **Q2FY27 (2026-05-01–2026-07-31, IN FLIGHT)**.
- **"Today" snapshot**: Monday, **2026-07-20**. Q2FY27 is 81 of 92 days elapsed
  (88.0%) — treat as quarter-to-date (QTD), never a closed quarter. Daily feeds land
  by 6am ET next day; the WBR (weekly business review) pack locks Monday 7am ET for
  the prior Sun–Sat week; MBR (monthly business review) reviews the prior fiscal
  month and is the point at which slow-moving quantitative signals actually get
  escalated (see SIGNAL [voc-leads-quant]).

### Vertical taxonomy (`dim_vertical`)

| vertical_code | name | sub-verticals | depth |
|---|---|---|---|
| US_CONV | US/CA/MX Conversion + Traffic | US, CA, MX (markets) | **DEEP** |
| MARKETPLACE | Marketplace | COLLECTIBLES, RESOLD, STYLE | **DEEP** |
| CARE | Customer Care | AUTOMATE, AVOID, OPTIMIZE, PLATFORM, W+ (member care) | **DEEP** |
| SPEED | Speed / Fulfillment | FD (fast delivery), PROMISE, EFFICIENCY | **DEEP** |
| MEMBERSHIP | Membership (Acme+) | — (this is the CLTV home vertical) | **DEEP** |
| CLUB | Club (warehouse-membership banner) | — | light |
| B2B | Acme Business (B2B/wholesale) | — | light |
| PAYMENTS | Payments | DS (dispute & settlement), MATCH (tender/ID match rate) | light |
| OPD_DFS | Online Pickup & Delivery — Delivery From Store | — | light |
| MARTECH | Retail media / marketing technology | — | light |
| MPCX | Marketplace Customer Experience | — | light |
| SPLITS | Order Splits (multi-shipment orders) | — | light |
| POR | Post-Order Returns | — | light |
| CSI | Customer Satisfaction Index (composite) | — | light |
| REVIEWS | Ratings & Reviews | — | light |
| FS_LATER | Financial Services — Pay Later (BNPL) | — | light |

Note (flag for Simon): the customer's redacted taxonomy list did not include a
standalone "Membership" row — only "W+" as a Care sub-program. I added MEMBERSHIP as
its own top-level vertical because the brief explicitly requires a 5th deep vertical
"where CLTV lives," and CLTV is a member-lifecycle concept, not a support-contact
concept. Care's own "W+" sub-program stays scoped to *support contacts from members*
(handling, CSAT); the separate MEMBERSHIP vertical owns signups/renewals/benefits/
CLTV. Two light verticals deliberately share underlying data with deep ones rather
than inventing parallel numbers: **OPD_DFS** reports off `fulfillment_speed_daily`
filtered to `fulfillment_type='dfs'`; **POR**'s headline "avg refund cycle days" is
the *same* series as Care's refund-cycle signal (see SIGNAL [por-care-shared]) — they
are one operational fact seen from two org lenses, and must always match.

### FY27 goals — actual/pace vs. target (as of "today," 2026-07-20)

| Metric | FY27 Target | Actual / Pace | % of goal | Status |
|---|---|---|---|---|
| Total digital + marketplace GMV | $7.53B | $7.62B run-rate (H1 +9.7% YoY, Q2 annualized) | 101.2% | AHEAD |
| US conversion rate (blended) | 3.35% | 3.22% (Q2FY27 QTD) | 96.1% | BEHIND |
| US sessions (traffic) | 1,650M | ~1,540M run-rate | 93.3% | BEHIND |
| Marketplace GMV | $3.32B | $3.89B run-rate | 117.1% | AHEAD |
| Care bot deflection rate (FY27 exit) | 50.0% | 52.1% (Q2FY27 QTD) | 104.2% | AHEAD *(CSAT caveat — SIGNAL)* |
| Speed blended on-time-to-promise (FY27 exit) | 93.5% | 93.00% (Q2FY27 QTD) | 99.5% | BEHIND *(mix-shift caveat — SIGNAL)* |
| Speed ship-to-home on-time-to-promise | 91.0% | 89.9% (Q2FY27 QTD) | 98.8% | BEHIND |
| Acme+ members (FY27 exit, 2027-01-31) | 14.8M | 14.62M, pacing ~15.05M | 101.7% | AHEAD |
| Acme+ annual renewal rate | 86.0% | 87.2% | 101.4% | BEAT |

FY26 actuals (full year, for YoY reference): Conversion-channel (US+CA+MX) GMV
$3,976.6M; Marketplace GMV $2,968.0M; **total $6,944.6M**.

---

## Arithmetic conventions — explicit, so downstream generators can't drift

1. **Conversion rate** = orders / sessions (session-based), always a %. **Orders**
   figures below are pre-computed as `ROUND(sessions × conversion_rate)`; treat the
   stated orders number as authoritative — hand-recomputing from the rounded rate may
   drift by a rounding hair, that's expected, don't "correct" the stated figure.
2. **GMV** = orders × AOV (average order value) per cut. Company-level GMV = SUM(US +
   CA + MX conversion-channel GMV) + SUM(Marketplace 3P GMV). These are two
   structurally different revenue types (1P/owned-inventory vs. 3P/marketplace
   commission-based) — never re-derive one from the other.
3. **Currency**: every `*_usd` column is already FX-converted to USD (fiscal-month-
   average rate). No local-currency (CAD/MXN) amounts are stored anywhere in this
   warehouse. Do not apply any further FX conversion to a `*_usd` column.
4. **Fiscal quarter boundaries** are calendar-month-aligned (see Company section).
   Q2FY27 is QTD (81/92 days, 88.0% elapsed) as of the snapshot date — never present
   a Q2FY27 figure as a closed-quarter total without saying QTD/pace.
5. **Sampling / panel convention (the load-bearing one).** Aggregate fact tables
   (`fact_traffic_daily`, `fact_promise_vs_actual`, `fact_experiment_exposures`,
   `fact_experiment_readouts`) are **full-population** for the modeled scope — their
   sums/counts ARE the real totals. Entity/event-grain tables (`dim_member`,
   `dim_seller`, `fact_orders`, `fact_care_contacts`, `fact_voc_responses`,
   `fact_marketplace_listings`, `fact_membership_events`) are **representative
   panels/samples** of a larger true population (stated per-table below). Rates and
   ratios computed on a panel (renewal %, CLTV/member, deflection %, seller return
   rate) are production-accurate. Absolute counts/totals (total members, total GMV,
   total contacts) must come from the aggregate marts or the Company-section figures
   — **never** from `COUNT(*)`/`SUM()` on a panel table. See SIGNAL
   [sample-vs-population] — this is the single most important convention in the
   document.
6. **BigQuery dataset is FLAT.** Every table — base and mart — is
   `nexus-analyst-demo.acme_ecomm.<table>`. No nested datasets. No
   `acme_ecomm.marts.*`, no `acme_ecomm.membership.*`.
7. **Experiment analysis** uses EXPOSED units (not merely assigned) as the effect-size
   denominator unless explicitly computing intent-to-treat (ITT). An
   assigned-but-never-exposed unit dilutes any ITT-basis read toward zero;
   `fact_experiment_exposures` carries both `units_assigned` and `units_exposed`
   specifically so this is checkable, not assumed.
8. **Authority hierarchy — quantitative**: Hive raw session/clickstream logs (legacy,
   pre-aggregation, hardest to query) < BigQuery base fact tables < BigQuery derived
   marts (canonical for that metric) < Company-section/MBR-deck stated figures
   (board-rounded, must reconcile to the marts, never contradict them).
   **Authority hierarchy — strategy/roadmap**: Slack/ad hoc chatter < Aitable cards
   (legacy ideation, pre-2026-01-15) < Confluence PRDs < Jira tickets (committed
   work, 2026-01-15 onward) < MBR decks (leadership-reviewed).
   **Authority hierarchy — qualitative (VOC)**: an individual Medallia verbatim
   (anecdote) < a theme-tagged aggregate report (pattern) < `fact_voc_responses`'
   canonical theme/score definitions (ground truth for "what does VOC say").

---

## Warehouse — `nexus-analyst-demo.acme_ecomm` (BigQuery, FLAT)

**24 tables** (updated from 23 — see `fact_seller_voc_responses`, flagged
below as a NEW TABLE): 8 dimensions + **10** base facts + 6 derived marts.

### Dimensions

- **dim_date**(date, fiscal_year, fiscal_quarter INT64, fiscal_quarter_label STRING
  e.g. `"Q1FY27"`, fiscal_week INT64, week_ending_date DATE, is_peak_holiday BOOL,
  day_of_week STRING, is_weekend BOOL). ~761 rows (2025-01-01..2027-01-31).
- **dim_vertical**(vertical_code STRING, vertical_name STRING, sub_vertical_code
  STRING NULLABLE, sub_vertical_name STRING NULLABLE, is_deep_dive BOOL,
  customer_facing_desc STRING). ~31 rows (16 verticals + sub-vertical rows).
- **dim_associate**(assoc_id STRING, full_name STRING, role STRING, team STRING,
  manager_assoc_id STRING NULLABLE, hire_date DATE, termination_date DATE NULLABLE,
  location STRING, is_active BOOL). ~180 rows — the corporate product/data/ops org
  relevant to these questions, NOT frontline store associates (those are out of
  scope for this warehouse).
- **dim_member**(member_id STRING, signup_date DATE, home_market STRING, plan_type
  STRING [`monthly`|`annual`], plan_price_usd NUMERIC, status STRING
  [`active`|`paused`|`cancelled`], cancel_date DATE NULLABLE, acquisition_channel
  STRING). **120,000-row representative panel** of the true ~14.2–14.6M active Acme+
  base (see SIGNAL [sample-vs-population]).
- **dim_fulfillment_node**(node_id STRING, node_type STRING
  [`dc`|`fc`|`store`|`sortation_center`|`returns_center`], node_name STRING, market
  STRING, opened_date DATE, store_format STRING NULLABLE [only for `store`:
  `supercenter`|`neighborhood`|`club`], is_active BOOL). ~180 rows.
- **dim_seller**(seller_id STRING, seller_name STRING, category_focus STRING
  [`collectibles`|`resold`|`style`|`other`], onboarded_date DATE,
  **application_date DATE NULLABLE — NEW COLUMN**, status STRING
  [`active`|`suspended`|`offboarded`], fulfillment_method STRING
  [`seller_fulfilled`|`ship_with_acme`], home_country STRING). **~2,560-seller
  panel** (Q2FY27) — three deliberate strata: top sellers by trailing-90d GMV +
  a random tail sample + a **new-seller funnel cohort** (~500 sellers, onboarded
  Q3FY26–Q4FY26 — chosen so every cohort member has at least ~5.6 months'
  runway to "today," 2026-07-20, before being scored on the funnel below;
  sellers onboarded in Q1FY27+ exist in the panel too but are excluded from
  the completed-funnel percentages as right-censored/still-maturing),
  deliberately oversampled so onboarding/churn analysis is
  representative — see "New-Seller Onboarding Funnel" under The Numbers and
  SIGNAL [seller-auth-friction]) — of a true active marketplace seller base of
  ~38,000. `application_date` is the date the seller *applied* to sell, distinct
  from `onboarded_date` (the date they were approved/went live); populated only
  for the new-seller funnel cohort (Q3FY26 onward) — NULL for earlier/legacy
  panel rows where it was never captured. Flag for Simon: this is a genuinely
  new column, not a rename — `onboarded_date` keeps its existing meaning
  everywhere it's already used.
- **dim_experiment**(experiment_id STRING, experiment_name STRING, vertical_code
  STRING, owner_assoc_id STRING, hypothesis STRING, start_date DATE, end_date DATE
  NULLABLE, status STRING [`running`|`shipped`|`killed`|`paused`], primary_metric
  STRING). ~85 rows across 6 quarters (full population).
- **dim_marketing_calendar**(event_id STRING, event_name STRING, event_type STRING
  [`campaign`|`launch`|`promo`|`holiday`|`budget_change`], vertical_code STRING
  NULLABLE, market STRING NULLABLE, start_date DATE, end_date DATE NULLABLE,
  planned_spend_usd NUMERIC NULLABLE, actual_spend_usd NUMERIC NULLABLE,
  owner_assoc_id STRING, notes STRING). ~140 rows (full population).

### Base facts

- **fact_traffic_daily**(date DATE, market STRING, vertical_code STRING,
  sub_vertical_code STRING NULLABLE, device STRING [`web`|`app`|`store_kiosk`],
  sessions INT64, sessions_definition_version INT64 [`1`=pre-2026-03-02,
  `2`=post], product_view_sessions INT64, add_to_cart_sessions INT64,
  checkout_started_sessions INT64, orders INT64, units INT64, gmv_usd NUMERIC).
  **Full population** (pre-aggregated grain — date × market × vertical × device).
- **fact_orders**(order_id STRING, order_date DATE, member_id STRING NULLABLE,
  market STRING, vertical_code STRING, sub_vertical_code STRING NULLABLE, channel
  STRING [`1P`|`3P`], seller_id STRING NULLABLE [set only when channel=`3P`],
  fulfillment_type STRING [`ship_to_home`|`bopis`|`curbside`|`dfs`], gmv_usd
  NUMERIC, units INT64, device STRING, is_returned BOOL, return_date DATE NULLABLE,
  return_reason_code STRING NULLABLE, refund_usd NUMERIC NULLABLE, refund_issued_date
  DATE NULLABLE). **Representative
  sample, ~400,000 rows** over the 6 quarters — used for member/seller/fulfillment-
  node joins. NOT the source for company-level GMV/order totals (see convention 5) —
  those come from `fact_traffic_daily` / the Company section.
- **fact_experiment_exposures**(experiment_id STRING, variant STRING, exposure_date
  DATE, units_assigned INT64, units_exposed INT64, units_converted INT64). **Full
  population** — aggregate grain (experiment × variant × date), not unit-level.
- **fact_experiment_readouts**(experiment_id STRING, variant STRING, as_of_date
  DATE, metric_name STRING, metric_value NUMERIC, sample_size_units INT64,
  lift_vs_control_pct NUMERIC NULLABLE, is_significant BOOL, notes STRING). Full
  population.
- **fact_promise_vs_actual**(date DATE, market STRING, vertical_code STRING,
  fulfillment_type STRING, orders_promised INT64, orders_on_time INT64,
  avg_days_late_when_late NUMERIC, node_id STRING NULLABLE). Full population,
  aggregate grain.
- **fact_care_contacts**(contact_id STRING, member_id STRING NULLABLE, order_id
  STRING NULLABLE, market STRING, sub_program STRING
  [`automate`|`avoid`|`optimize`|`platform`|`member_care`], channel STRING
  [`chat`|`phone`|`bot`|`email`], opened_at TIMESTAMP, closed_at TIMESTAMP
  NULLABLE, deflected BOOL, deflection_type STRING NULLABLE, resolution_code
  STRING, csat_score INT64 NULLABLE [1-5], handle_time_minutes NUMERIC NULLABLE,
  assoc_id STRING NULLABLE [null if bot-only]). **Representative sample, ~50,000
  rows** over 6 quarters.
- **fact_marketplace_listings**(listing_id STRING, seller_id STRING, category
  STRING [`collectibles`|`resold`|`style`|`other`], listed_date DATE, price_usd
  NUMERIC, status STRING [`active`|`removed`|`suspended`], authenticity_verified
  BOOL). **Representative sample, ~35,000 rows** (tied to the ~2,500-seller panel).
- **fact_membership_events**(event_id STRING, member_id STRING, event_date DATE,
  event_type STRING
  [`signup`|`renewal`|`cancel`|`pause`|`resume`|`benefit_redeemed`], benefit_code
  STRING NULLABLE, channel STRING). **~450,000 rows** (lifecycle + benefit-
  redemption events for the 120K-member panel over 6 quarters).
- **fact_voc_responses**(response_id STRING, member_id STRING NULLABLE, order_id
  STRING NULLABLE, market STRING, vertical_code STRING NULLABLE, survey_type
  STRING [`post_purchase`|`post_care_contact`|`nps`], responded_at TIMESTAMP,
  score NUMERIC, score_type STRING [`nps_0_10`|`csat_1_5`|`ces_1_7`],
  verbatim_text STRING, theme_tag STRING NULLABLE, sentiment STRING
  [`positive`|`neutral`|`negative`]). **Representative sample, ~40,000 rows.**
  This is **buyer-side VOC only** (Medallia) — it never carries a seller theme
  or a seller respondent; see `fact_seller_voc_responses` below for the
  seller-side stream. The two must never be blended into one "VOC" query.
- **fact_seller_voc_responses**(response_id STRING [`svoc_` prefix — a
  namespace deliberately distinct from buyer VOC's `voc_` prefix], seller_id
  STRING, survey_type STRING [`onboarding_pulse_l1`|`onboarding_pulse_l5`
  |`onboarding_pulse_l10`|`quarterly_seller_nps`], responded_at TIMESTAMP,
  score NUMERIC, score_type STRING [`seller_nps_0_10`|`ces_1_7`],
  verbatim_text STRING, theme_tag STRING NULLABLE, sentiment STRING
  [`positive`|`neutral`|`negative`]). **NEW TABLE.** Seller-side VOC — a fully
  separate stream from `fact_voc_responses`, per the customer's own framing
  (buyer and seller are separate orgs with separate feedback loops): different
  instrument ("Seller Pulse," adapter `seller_pulse_survey`, not Medallia),
  different cadence (triggered at listing-count milestones 1/5/10, plus a
  standing quarterly NPS — vs. buyer VOC's per-order/per-care-contact cadence),
  and its own theme vocabulary (`authentication-friction`,
  `listing-setup-complexity`, `no-performance-visibility` — see SIGNAL
  [seller-auth-friction]). A seller theme must never appear on a
  `fact_voc_responses` row, and a buyer theme (e.g. `refund delay`,
  `listing-accuracy-gap`) must never appear here. **Representative panel,
  ~4,000 rows** — scoped to the ~2,560-seller panel, proportionally much
  smaller than buyer VOC's ~40,000 (matching the much smaller seller
  population, ~38,000 true sellers vs. ~14.6M members/shoppers).

### Derived marts

- **traffic_conversion_summary**(fiscal_week_ending DATE, market STRING,
  vertical_code STRING, sessions INT64, sessions_definition_version INT64, orders
  INT64, conversion_rate NUMERIC, gmv_usd NUMERIC, orders_yoy_pct NUMERIC
  NULLABLE). Board source for conversion/traffic; carries the definition-version
  flag forward on purpose (does NOT silently paper over the 2026-03-02 cutover).
- **fulfillment_speed_daily**(date DATE, market STRING, vertical_code STRING,
  fulfillment_type STRING, orders_promised INT64, on_time_rate NUMERIC,
  pct_of_total_orders NUMERIC, avg_cost_per_order_usd NUMERIC). Board source for
  Speed; the `pct_of_total_orders` (mix share) column is what makes the mix-shift
  SIGNAL checkable — it is present precisely so a careful reader isn't fooled by
  the blended rate alone.
- **care_deflection_daily**(date DATE, sub_program STRING, contact_volume INT64,
  deflection_rate NUMERIC, avg_csat_deflected NUMERIC, avg_csat_agent_assisted
  NUMERIC, avg_handle_time_minutes NUMERIC). Board source for Care.
- **member_cltv**(member_id STRING, signup_cohort_quarter STRING, tenure_days
  INT64, lifetime_orders INT64, lifetime_gmv_usd NUMERIC, trailing_12mo_gmv_usd
  NUMERIC, trailing_12mo_orders INT64, benefits_adopted_count INT64, is_active
  BOOL, projected_cltv_usd NUMERIC). Board source for CLTV. **Canonical build uses
  LEFT JOIN `dim_member` to `fact_orders` + `COALESCE(trailing_12mo_gmv_usd, 0)`** —
  see SIGNAL [cltv-join-drop]. An INNER JOIN silently drops the panel's dormant
  (zero-trailing-order) members.
- **marketplace_seller_performance**(seller_id STRING, category_focus STRING,
  active_listings INT64, trailing_90d_gmv_usd NUMERIC, return_rate NUMERIC,
  avg_days_to_ship NUMERIC, authenticity_flag_count INT64, avg_buyer_rating
  NUMERIC). Board source for Marketplace seller health.
- **marketplace_gmv_summary**(fiscal_week_ending DATE, sub_vertical_code STRING,
  gmv_usd NUMERIC, orders INT64, take_rate NUMERIC). **Full population** — the
  canonical source for Marketplace GMV-by-sub-vertical; the quarterly Style/
  Resold/Collectibles GMV series in the Numbers section rolls up from this
  mart. Never `SUM(gmv_usd) GROUP BY sub_vertical_code` on `fact_orders` for
  this cut — `fact_orders` is the ~400,000-row sample (convention 5); this mart
  is the full-population aggregate the convention requires.

---

## The numbers — quarterly series (Q1FY26 → Q2FY27, last is QTD)

### US/CA/MX Conversion + Traffic (US_CONV, deep)

| Market | Metric | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 QTD |
|---|---|---|---|---|---|---|---|
| US | sessions (M) | 402.0 | 418.5 | 437.0 | 598.0 | 379.5 | 308.0 |
| US | conversion % | 3.05 | 3.00 | 3.10 | 3.92 | 3.18 | 3.22 |
| US | orders (M) | 12.261 | 12.555 | 13.547 | 23.442 | 12.068 | 9.918 |
| US | AOV $ | 53.10 | 53.60 | 54.20 | 58.40 | 54.90 | 55.60 |
| US | GMV ($M) | 651.1 | 672.9 | 734.2 | 1,369.0 | 662.5 | 551.4 |
| CA | sessions (M) | 44.62 | 46.45 | 48.51 | 66.38 | 42.12 | 34.19 |
| CA | conversion % | 2.95 | 2.90 | 3.00 | 3.82 | 3.08 | 3.12 |
| CA | GMV ($M) | 74.79 | 77.26 | 84.39 | 158.45 | 76.22 | 63.46 |
| MX | sessions (M) | 28.54 | 29.71 | 31.03 | 42.46 | 26.94 | 21.87 |
| MX | conversion % | 2.50 | 2.45 | 2.55 | 3.37 | 2.63 | 2.67 |
| MX | GMV ($M) | 28.80 | 29.66 | 32.59 | 63.51 | 29.57 | 24.67 |
| **Total conv. GMV ($M)** | | **754.6** | **779.9** | **851.2** | **1,590.9** | **768.3** | **639.5** |

YoY, Q1FY27 vs Q1FY26 (US): sessions **-5.6%**, orders **-1.6%** (conversion rate
improved YoY, partly offsetting the traffic decline — but see SIGNAL
[session-definition]: part of that conversion "improvement" is measurement, not
behavior). MX has run persistently ~0.4-0.6pp below CA and ~0.5-0.9pp below US
across **all 6** modeled quarters — a stable structural gap, not a trend (deliberately
not a signal — see DISTRACTORS / QUESTIONS.md Q14).

#### US Conversion — weekly detail (Q2FY27, the live WoW question)

`fact_traffic_daily` is full-population daily grain, so a weekly (Sun–Sat, WBR
convention) cut is always computable underneath the quarterly table above — the
Q2FY27 QTD figure (3.22%) is an average across ~11.6 elapsed weeks, not a
single measurement, and a single week can move well beyond the quarterly
average without contradicting it.

| Week ending (Sun–Sat) | US sessions (M) | Device mix web/app/kiosk | Device conv. web/app/kiosk | Blended conv. % |
|---|---|---|---|---|
| 2026-07-11 | 26.80 | 69.0% / 28.0% / 3.0% | 4.00% / 1.50% / 2.00% | 3.24 |
| 2026-07-18 | 26.40 | 59.4% / 37.6% / 3.0% | 3.76% / 1.50% / 2.00% | 2.86 |

Orders: 868,320 (week of 07-11) → 755,038 (week of 07-18). **Week-over-week:
-0.38pp (≈ "down 40bps"), 3.24% → 2.86%.** Shift-share decomposition (rates
fixed at week-0 levels to isolate the mix effect, then shares fixed at week-1
levels for the rate effect — the two sum exactly to the observed move):
**mix effect ≈ -0.24pp** (app's session share jumped 28.0%→37.6%, and app
converts structurally lower than web — a mix shift with *zero* real behavior
change would already produce most of this move) and **rate effect ≈ -0.14pp**
(a genuine web-conversion softening, 4.00%→3.76%). The rate effect is real but
modest, and — see SIGNAL [roadmap-doesnt-explain-it] — neither the shipped-launch
roadmap nor the net effect of in-flight experiments (SIGNAL
[offsetting-experiments]) explains it; it sits inside ordinary week-to-week
variation once mix-shift is accounted for, and the honest answer does not
force a tidier story onto that remainder. Medallia verbatims tagged to item-page
sessions in this window skew toward the new autoplay media module feeling
"cluttered" / "the video just starts and it's annoying" / "page feels slower
now" — low volume, not yet a top theme, but directly on-point for the
shopper-meaning half of the answer (see SIGNAL [offsetting-experiments] for the
module itself).

A same-week marketing-calendar launch — "Homepage Hero Banner Refresh"
(2026-07-13, homepage-only, owner maya.lindqvist) — is a coincidental-timing
distractor: no item-page or search overlap, and query-log/FullStory review
around it shows no measurable conversion effect. See SIGNAL
[roadmap-doesnt-explain-it] and DISTRACTORS.

#### Item Page surface — Q1FY27 detail (the "simple question," US_CONV)

Two distinct, both-legitimate "item page" metrics, at product-view-session
grain (`product_view_sessions` in `fact_traffic_daily`, ~62% of US sessions,
≈235.3M of Q1FY27's 379.5M):

- **View-to-cart rate** = `add_to_cart_sessions / product_view_sessions` — an
  engagement metric, purchase-independent.
- **Item-page-scoped conversion** = `orders / product_view_sessions` — a
  *different, larger* number than the standard site conversion rate
  (`orders / sessions`, 3.18% for Q1FY27) because the denominator excludes
  browse-only sessions that never reached a product page:
  **12.068M / 235.3M = 5.13%** for Q1FY27. Neither figure is "wrong" — they
  answer different questions ("of everyone who came, how many bought" vs. "of
  everyone who engaged with a product, how many bought") — state which one
  you're using and why. See SIGNAL [item-page-metric-choice].

Q1FY27 also carries the **same** `sessions_definition_version` 1→2 cutover
(2026-03-02) that affects the top-line conversion number (SIGNAL
[session-definition]): because `product_view_sessions` and
`add_to_cart_sessions` live in the same `fact_traffic_daily` row, the identical
bot/dedup fix mechanically affects both item-page metrics too, not just the
site-wide rate. View-to-cart rate: **18.0%** (pre-cutover, version 1, Feb 1–Mar
1, ~29 days) → **19.9%** (post-cutover, version 2, Mar 2–Apr 30, ~60 days) — a
raw **+1.9pp** move of which **≈+0.8pp is the same definitional/mechanical
bump** as the site-wide metric and **≈+1.1pp is real**, plausibly attributable
to the Item Page Iteration Program (6 shipped iterations across the quarter —
timeline 2026-02-05 through 2026-04-16, owner maya.lindqvist; iterations v3-v6
shipped post-cutover, v1-v2 pre-cutover, so their individual effects sit on
different measurement bases too). Silently averaging view-to-cart rate across
the whole quarter overstates the "real," iteration-driven improvement by
roughly 40% relative. See SIGNAL [item-page-metric-choice].

### Marketplace (MARKETPLACE, deep) — GMV ($M) by sub-vertical

| Sub-vertical | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 QTD |
|---|---|---|---|---|---|---|
| Style | 512.0 | 530.0 | 549.0 | 715.0 | 543.0 | 444.1 |
| Resold | 88.0 | 97.0 | 109.0 | 142.0 | 168.0 | 143.1 |
| Collectibles | 22.0 | 25.0 | 61.0 | 118.0 | 104.0 | 91.2 |
| **Total** | **622.0** | **652.0** | **719.0** | **975.0** | **815.0** | **678.4** |

Style Q1FY27 YoY: **+6.1%** (vs. ~10% planned trend — the "deceleration"). Resold
Q1FY27 YoY: **+90.9%**. Collectibles Q1FY27 YoY: **+372.7%** (small base; boom
ignited Q3FY26, +144.0% QoQ). Resold's apparel/style-adjacent category share: **51%**
(year-ago) → **62%** (Q1FY27) — see SIGNAL [marketplace-cannibalization]. Sellers (dim_seller panel — 2,560 tracks the panel
size, not the ~38,000-seller true population): 1,980 → 2,560 over the 6 quarters.
Take rate: 13.2% → 13.6%. Return rate,
Collectibles: 9.8% → 11.2% (Q3FY26 counterfeit spike) → **5.4%** (Q2FY27, post-Acme
Verified). Q4FY26 Marketplace GMV was flash-reported at $952.4M at quarter-close,
later restated to the canonical **$975.0M** (see DISTRACTORS).

#### New-Seller Onboarding Funnel (US-7: seller side)

Stage-based, **listing-count** cohort (not calendar-tenure) — a seller's stage
is how many listings they've posted, not how long ago they onboarded. Cohort:
the ~500-seller new-seller stratum of the `dim_seller` panel (`application_date`
populated, onboarded Q3FY26–Q4FY26 — at least ~5.6 months' runway to "today,"
so a seller who was going to reach listing 10 has had time to). 200
Collectibles + 150 Resold + 150 Style (B2B has no 3P sellers — this funnel is
Marketplace-only). Sellers onboarded Q1FY27+ are in the panel but
right-censored — too new to score on the completed funnel below.

| Stage | Collectibles (n=200) | Resold (n=150) | Style (n=150) |
|---|---|---|---|
| Applied → onboarded (listing 1) | 100% (200) | 100% (150) | 100% (150) |
| Reached listing 5 | 46% (92) | 74% (111) | 76% (114) |
| Reached listing 10 | **24% (48)** | 46% (69) | 48% (72) |
| Sustained (10+ listings AND ≥1 new listing in trailing 90d) | 19% (38) | 40% (60) | 42% (63) |

Style and Resold show the same broad shape (churn concentrated before listing
10, roughly half the cohort never gets there) — Collectibles is **structurally
worse at every stage**, with its steepest relative drop happening earliest
(listing 1→5). Root cause, tied to existing canon rather than a new one: the
**"Acme Verified" authentication program** (GradeSure partnership, launched
2025-09-08 after the counterfeit spike, badge shipped to 100% of Collectibles
listings 2025-11-20) requires each new listing to clear GradeSure
authentication before it carries the badge — and the badge itself is what the
"Verified Badge Prominence" experiment already proved is worth **+6.8%**
conversion (2025-11-15 readout). An unverified listing is materially
uncompetitive, so authentication isn't optional in practice, but it costs a
new seller real per-item time/fee/latency that an established seller has
already amortized. **Verification-speed split, Collectibles cohort**: of the
200, 120 (60%) get their debut listing verified within 7 days — that group
reaches listing 10 at **30%** (36 sellers); the other 80 (40%, slower/no early
verification) reach listing 10 at **15%** (12 sellers) — verified-within-7-days
sellers clear listing 10 at 2x the rate (36+12=48, reconciling to the 24%
cohort figure above). This is the buyer/seller tension made concrete and
measurable on **both** sides from data already in canon: the *same* program
took Collectibles' return rate from 11.2% (Q3FY26 peak) to **5.4%** (Q2FY27) —
a real buyer-trust win protecting a $91.2M/quarter (Q2FY27 QTD), +372.7%-YoY
category — while measurably suppressing new-seller survival in that exact
category. See SIGNAL [seller-auth-friction].

**Seller-side VOC** (`fact_seller_voc_responses` — a separate stream from
buyer Medallia, see Warehouse section): among Collectibles onboarding-pulse
(L1/L5) respondents, **`authentication-friction` is the dominant theme at
~38%** of verbatims, vs. ~5% for Style and ~6% for Resold onboarding-pulse
respondents (authentication isn't a Style/Resold pain point — those
categories don't require it). Two *other* seller themes are category-agnostic,
present at similar levels across all three: **`listing-setup-complexity`**
(~15-20% each — no bulk-upload/duplicate-listing tooling, hits hardest between
listing 1 and 5) and **`no-performance-visibility`** (~12-18% each — sellers
can't see why an existing listing isn't converting, concentrated in the
listing 5-10 range, i.e., sellers who pushed through the setup phase but can't
tell what to fix next). These two map directly onto the two named seller
surfaces: `listing-setup-complexity` → **seller listing**; `no-performance-
visibility` → **seller optimization**. Owning PM: camille.duarte (see ORG).

**Listing-quality signal** (existing `fact_marketplace_listings.status` and
`authenticity_verified` columns, no new column needed): a new seller's early
listings landing in `status='removed'` (quality/compliance removal) correlates
with churn across all three categories, independent of the authentication
story above.

**Seller-side "conversion" is a different metric than buyer-side conversion**
— sell-through (orders/units per **active listing**, from the existing
`marketplace_seller_performance` mart's `active_listings` +
`trailing_90d_gmv_usd`/order count), not orders per **session**. Illustrative:
Collectibles new sellers (first 90 days) average **1.8 orders per active
listing per quarter**, vs. **3.6** for tenured (12mo+) Collectibles sellers — a
second, reinforcing (not competing) explanation for early discouragement,
alongside the authentication-friction story. A question asking for "seller
conversion" without specifying which side must not be answered with the
buyer-side `orders/sessions` figure.

### Care (CARE, deep)

| Metric | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 QTD |
|---|---|---|---|---|---|---|
| Contacts (K) | 2,150 | 2,205 | 2,280 | 3,650 | 2,050 | 1,180 |
| Deflection % | 37.2 | 39.5 | 42.8 | 45.0 | 49.6 | 52.1 |
| CSAT, deflected | 3.90 | 3.85 | 3.80 | 3.70 | 3.42 | 3.55 |
| CSAT, agent-assisted | 4.30 | 4.32 | 4.35 | 4.20 | 4.30 | 4.31 |
| Avg handle time (min) | 8.4 | 8.2 | 8.0 | 9.1 | 7.6 | 7.4 |

`avg_refund_cycle_days` = AVG(`refund_issued_date` − `return_date`) over returned
orders in `fact_orders`, rolled up to a 4-week trailing average — this is the one
metric POR and Care both report (see SIGNAL [por-care-shared]); it is not a separate
warehouse table, just a different org lens on the same `fact_orders` columns.
Weekly refund-cycle-days / Medallia "refund delay" verbatim-share (Nov 2025–Mar
2026) — the VOC-leads-quant signal: baseline VOC share ~3.5%; crosses **10%** the
week of **2025-12-15** (11.2%); peaks **16.1%** week of 2026-01-05. The quantitative
4-week-rolling `avg_refund_cycle_days` crosses its **5.0-day SLA alert threshold**
the week of **2026-01-05** (5.03) — 3 weeks after VOC. Formal escalation happens at
the **2026-02-02 MBR** (monthly cadence) — **7 weeks** after VOC first flagged it.
Root cause: Ontario, CA returns-processing center (`node_id` in `dim_fulfillment_node`,
`node_type='returns_center'`) ran ~22% understaffed through peak (a hiring-freeze
exception that should have applied to it didn't); fixed post-escalation, metric back
to ~3.3 days by mid-March 2026.

### Speed / Fulfillment (SPEED, deep)

| Metric | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 QTD |
|---|---|---|---|---|---|---|
| Ship-to-home mix % | 77.5 | 76.5 | 75.4 | 74.0 | 68.9 | 66.8 |
| Pickup (BOPIS+curbside) mix % | 21.0 | 22.0 | 23.0 | 24.0 | 29.0 | 31.0 |
| DFS mix % | 1.5 | 1.5 | 1.6 | 2.0 | 2.1 | 2.2 |
| Ship-to-home on-time % | 89.5 | 89.9 | 90.1 | 87.0 | 89.3 | 89.9 |
| Pickup on-time % | 99.5 | 99.4 | 99.5 | 99.1 | 99.6 | 99.6 |
| DFS on-time % | 93.0 | 93.2 | 93.0 | 90.5 | 93.8 | 94.2 |
| **Blended on-time %** | **91.65** | **92.04** | **92.31** | **89.97** | **92.38** | **93.00** |
| Cost per order ($) | 7.85 | 7.78 | 7.70 | 8.60 | 7.55 | 7.30 |

Blended on-time is a weighted average of the three channel rates by mix share —
always derivable from the two rows above it; never state a blended figure that
doesn't reconcile. Q1FY26→Q1FY27: blended **+0.73pp**, ship-to-home **-0.20pp**,
pickup mix **+8.0pp** — the entire blended gain is mix-shift (SIGNAL
[otp-mix-shift]). Q4FY26's dip (89.97% blended, 87.0% ship-to-home) = peak-volume
strain plus a December winter-storm disruption at the JOL1 DC (timeline).

### Membership — Acme+ (MEMBERSHIP, deep)

| Metric | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 QTD |
|---|---|---|---|---|---|---|
| Members, true base (M, end of period) | 12.60 | 12.90 | 13.35 | 13.95 | 14.35 | 14.62 |
| Net adds (K) | 310 | 300 | 450 | 600 | 400 | 270 |
| Annual renewal rate % | 86.2 | 86.4 | 86.7 | 86.9 | 87.0 | 87.2 |

Net-adds are exact deltas of the true-base row — reconcile before using either
independently. **CLTV mart join trap** (120,000-member panel): 20% (24,000) have
**zero orders** in the trailing 12 months (dormant, still paying/active).
INNER-JOIN (wrong) average CLTV = **$625/member** (computed only on the 80% who
ordered). LEFT JOIN + COALESCE(0) (correct) average CLTV = **$500/member** — the
wrong number overstates CLTV by exactly 25% and hides the dormant population
entirely. **Benefit adoption → renewal**: 0 extra benefits (free shipping only) =
71% renewal; 1 benefit = 89%; 2+ benefits = 95%. Streaming-bundle users
specifically = 93% renewal even alone, but only **34%** of members know they have
the benefit. That 93% is a category-level read spanning both streaming partners —
the benefit itself dates to 2025-06-01 (Vidora, switched to Reelstream 2026-06-01,
just 7 weeks before "today"); Reelstream's own retention isn't independently
validated yet (see Q13 on the ~12-month cohort lag).

---

## Dated timeline of events (Q1FY26 → Q2FY27)

Every document generated for this corpus must be consistent with — and free to
reference — this timeline. Dates, owners, and verticals are canon.

| Date | Event | Vertical | Owner |
|---|---|---|---|
| 2025-02-01 | FY26 begins | — | — |
| 2025-03-10 | carlos.figueroa promoted Director → VP Data & Analytics | Data | carlos.figueroa |
| 2025-05-14 | ReWear Collective (sel_500204) crosses $1M trailing-90d GMV, becomes a top-20 Resold seller | Marketplace | victor.okonkwo |
| 2025-06-01 | Acme+ streaming perk begins under original partner "Vidora" (pre-canon; superseded 2026-06-01) | Membership | renee.kowalski |
| 2025-06-15 | malik.hendon hired as Sr PM Acme Business (B2B/Wholesale), assoc_100160 — B2B's first dedicated PM | B2B | felix.arroyo |
| 2025-08-04 | Counterfeit-listing spike detected in Collectibles (viral vintage-card auction result triggers a flood of new sellers/buyers, some bad-faith) | Marketplace | lucia.ferreira |
| 2025-08-12 | Bramblewood Vintage (sel_500089) flagged for 3 counterfeit-listing violations | Marketplace | lucia.ferreira |
| 2025-09-01 | lucia.ferreira hired/starts as Trust & Safety Lead, Marketplace (urgent backfill in response to 08-04) | Marketplace | victor.okonkwo |
| 2025-09-02 | Bramblewood Vintage (sel_500089) suspended pending compliance review | Marketplace | lucia.ferreira |
| 2025-09-08 | "Acme Verified" authentication program launches (partner: GradeSure) | Marketplace | lucia.ferreira |
| 2025-09-15 | "Ask Acme v2" care bot launches | Care | dominic.paquet |
| 2025-09-20 | Fall Savings Acme+ join promo begins (through 2025-10-15) | Membership | simone.laurent |
| 2025-10-01 | "Verified Badge Prominence" experiment (`exp_2401`) starts, Collectibles | Marketplace | sanjay.bhatt |
| 2025-11-01 | Q4FY26 (peak/holiday quarter) begins | — | — |
| 2025-11-15 | "Verified Badge Prominence" experiment ends; +6.8% conversion lift, no confound | Marketplace | sanjay.bhatt |
| 2025-11-20 | Verified Badge shipped to 100% of Collectibles listings | Marketplace | sanjay.bhatt |
| 2025-11-28 | Black Friday | US_CONV / all | maya.lindqvist |
| 2025-12-01 | Cyber Monday week; refund-cycle-days begins climbing (retro-identified root cause: Ontario returns center understaffing) | Care / POR | hannah.brennan |
| 2025-12-08 | Winter storm disrupts JOL1 (Joliet) DC for 36 hours | Speed | gabriel.stroud |
| 2025-12-15 | Medallia "refund delay" verbatim theme crosses 10% share (first VOC flag) | Care | giulia.romano |
| 2026-01-05 | Quantitative 4-week-rolling avg_refund_cycle_days crosses 5.0-day SLA threshold | Care / POR | hannah.brennan |
| 2026-01-12 | "Wider Promise Window" experiment (`exp_1187`) starts, US | Speed | leo.brandt |
| 2026-01-12 | DC sortation automation Phase 1 begins at FON2 (Fontana) + JOL1 (Joliet), phased through 02-15 | Speed | gabriel.stroud |
| 2026-01-15 | Pickup Perks BOPIS/curbside discount campaign launches | Speed | tara.oduya |
| 2026-01-15 | Aitable → Jira roadmap consolidation project kicks off (not complete as of "today") | Product Ops | nadia.esposito |
| 2026-01-15 | Bramblewood Vintage (sel_500089) reinstated after compliance review | Marketplace | lucia.ferreira |
| 2026-01-31 | FY26 ends | — | — |
| 2026-02-01 | FY27 begins | — | — |
| 2026-02-02 | Refund-cycle-days SLA breach formally escalated at MBR; Ontario staffing root-caused | Care / POR | hannah.brennan |
| 2026-02-04 | Paid-search budget cut (-18%, marketing-efficiency initiative) begins | Martech / US_CONV | felix.arroyo (approves growth-marketing spend) |
| 2026-02-05 | Item Page Iteration v1 (above-fold price/CTA reflow) ships | US_CONV | maya.lindqvist |
| 2026-02-16 | "Checkout Simplify" experiment (`exp_2214`) starts, US | US_CONV | owen.faust |
| 2026-02-19 | Item Page Iteration v2 (reviews section reorder) ships | US_CONV | maya.lindqvist |
| 2026-02-20 | "Wider Promise Window" experiment ends; confounded full-window read +4.2pp OTP | Speed | leo.brandt |
| 2026-02-20 | Ontario returns center back to full staffing | Care | hannah.brennan |
| 2026-03-01 | "Nav Refresh" sitewide redesign launches (both experiment arms), with a 5%-of-traffic 3-week holdback (`exp_2215`) | US_CONV | maya.lindqvist |
| 2026-03-02 | Session-counting fix ships: bot/dup filtering, `sessions_definition_version` 1→2 | US_CONV | wei.hartono |
| 2026-03-02 | "Wider Promise Window" killed (net-negative once deconfounded) | Speed | tara.oduya |
| 2026-03-05 | Item Page Iteration v3 (image gallery zoom/swipe) ships — first iteration on `sessions_definition_version` 2 | US_CONV | maya.lindqvist |
| 2026-03-19 | Item Page Iteration v4 (size/fit guidance module) ships | US_CONV | maya.lindqvist |
| 2026-03-21 | Nav Refresh holdback readout completes: independent +1.3% conversion lift, sitewide | US_CONV | maya.lindqvist |
| 2026-03-30 | "Checkout Simplify" experiment ends; full-window read +2.1% (confounded), pre-confound (Feb16-28) read +0.8% | US_CONV | owen.faust |
| 2026-04-01 | "Bot Handoff Threshold" experiment (`exp_2489`) starts, Care | Care | aisha.rahman |
| 2026-04-02 | Item Page Iteration v5 (cross-sell module placement) ships | US_CONV | maya.lindqvist |
| 2026-04-06 | Checkout Simplify shipped to 100% (decision made on the confounded +2.1% figure) | US_CONV | owen.faust |
| 2026-04-08 | camille.duarte joins as Sr PM Marketplace Seller Experience (Listings & Optimization), assoc_100123 | Marketplace | victor.okonkwo |
| 2026-04-16 | Item Page Iteration v6 (sticky add-to-cart bar, mobile) ships — last of 6 iterations this quarter | US_CONV | maya.lindqvist |
| 2026-04-20 | "Seller Pulse" onboarding-survey program launches (listing-milestone + quarterly-NPS cadence), `fact_seller_voc_responses` begins populating | Marketplace | camille.duarte |
| circa 2026-Q1 (undated draft) | "Style Conversion Recovery Plan" drafted (Confluence), proposing Trust & Safety headcount move off Collectibles onto Style | Marketplace | ines.delgado (draft), never actioned |
| 2026-05-01 | "Benefit Onboarding Carousel" experiment (`exp_2556`) starts, Membership | Membership | derek.holloway |
| 2026-05-15 | "Bot Handoff Threshold" experiment ends; +3pp deflection, -0.15 CSAT among late-escalated users | Care | aisha.rahman |
| 2026-05-20 | Bot Handoff Threshold partially shipped (non-billing categories only) | Care | aisha.rahman |
| 2026-06-01 | Acme+ streaming perk switches partner: Vidora → Reelstream | Membership | renee.kowalski |
| 2026-06-08 | "Search Relevance Re-ranking" experiment (`exp_2601`) starts, US | US_CONV | owen.faust |
| 2026-06-08 | "Item Page Media Carousel Autoplay" experiment (`exp_2618`) starts, US | US_CONV | maya.lindqvist |
| 2026-06-15 | "Benefit Onboarding Carousel" experiment ends; +9pp 30-day benefit awareness (renewal-rate readout not yet valid — needs ~12mo/cohort) | Membership | derek.holloway |
| 2026-07-13 | "Homepage Hero Banner Refresh" launches (homepage-only, no item-page/search overlap) | US_CONV | maya.lindqvist |
| 2026-07-20 | **"Today" — snapshot date** | — | — |

---

## CROSS-VERTICAL BACKLOG SNAPSHOT (Jira/Aitable, "as of today") — the unstaffed blind spot

Buyer-side Medallia verbatims mention listings' photos/descriptions not
matching true scale, condition, or specification at a non-trivial share in
**all four** of these verticals — a *steady-state* pattern (roughly flat for
the past 2-3 quarters, not a rising trend like [voc-leads-quant]) —
theme_tag `listing-accuracy-gap`: **Style 14%**, **Resold 12%**,
**Collectibles 9%**, **B2B 22%** (bulk-order buyers, spec-sheet/pallet-config
mismatches) of each vertical's post-purchase verbatims. No single PM sees the
pattern because each only reads their own vertical's VOC report.

The backlog below is deliberately **complete** (every open initiative each
PM/vertical currently owns) so the absence is provable, not merely unstated:

**Style** (owner ines.delgado): (1) size-chart standardization across supplier
catalogs, (2) promo-calendar automation for flash sales, (3) influencer/UGC
content licensing pilot, (4) category-page filters for sustainability/material
tags, (5) returns-reason taxonomy cleanup (joint w/ POR).

**Resold** (owner noah.kessler): (1) condition-grading rubric v2 (seller
self-assessment), (2) trade-in/buyback pilot for owned inventory, (3)
authentication-partnership scoping (apparel-focused, non-GradeSure), (4)
seller payout-speed improvement, (5) category-mix reporting for the
Style wallet-share shift (the Q5/Q6 finding).

**Collectibles** (owner sanjay.bhatt): (1) GradeSure SLA renegotiation
(turnaround time), (2) counterfeit-detection ML model v2, (3) verified-badge
visibility expansion into search results, (4) grading-fee subsidy pilot **for
top-100 sellers** (note: aimed at established sellers, not the new-seller
cohort — see New-Seller Onboarding Funnel), (5) category-taxonomy expansion
(trading cards → memorabilia subtypes).

**B2B** (owner malik.hendon): (1) bulk-order quoting tool v2, (2) net-30
invoicing automation, (3) wholesale-catalog API for procurement-system
integration, (4) volume-discount tier restructuring, (5) account-rep coverage
model review.

**None of these 20 items addresses listing photo/description/spec accuracy.**
It sits adjacent to several (Style's UGC content pilot, Resold's
condition-grading rubric, Collectibles' badge-visibility work, B2B's catalog
API) without any of them actually owning it. Recommended owner: **no one owns
it today** — the closest fit is camille.duarte (Sr PM Marketplace Seller
Experience, listings-side), sponsored by victor.okonkwo (SVP Marketplace, the
only role spanning all three Marketplace sub-verticals) for the Marketplace
slice, coordinating with malik.hendon for the B2B slice. See SIGNAL
[listing-accuracy-blind-spot].

---

## SIGNALS — correct buried truths (state VERBATIM-accurate; scatter through noise)

- **[session-definition]** Sessions counting changed 2026-03-02 (bot/crawler
  filtering + multi-tab de-duplication); `sessions_definition_version` 1→2. This
  mechanically raises measured conversion rate (same orders, smaller denominator)
  independent of real behavior. Never compare sessions/conversion across the
  boundary date without noting the version — `traffic_conversion_summary` carries
  the flag forward on purpose, it does not adjust for you.
- **[paid-search-cut]** The real driver of Q1FY27's US session decline (-5.6% YoY)
  is an 18% paid-search budget cut (Martech, starting 2026-02-04), a deliberate
  marketing-efficiency move — not a demand-side or competitive problem.
- **[checkout-confound]** "Checkout Simplify" (`exp_2214`, 2026-02-16 to 2026-03-30)
  full-window readout (+2.1% conversion) is confounded by "Nav Refresh" launching
  into both arms 2026-03-01. Nav Refresh's own holdback-measured independent lift is
  +1.3% sitewide. The clean pre-confound slice (Feb16-28) reads +0.8%. Shipped
  2026-04-06 on the confounded number regardless.
- **[wider-window-confound]** "Wider Promise Window" (`exp_1187`, 2026-01-12 to
  2026-02-20) full-window readout (+4.2pp on-time-hit-rate) is confounded by
  concurrent DC sortation automation (FON2 + JOL1, phased 2026-01-12 to 2026-02-15).
  Isolated/deconfounded effect: +1.5pp, alongside a real -0.6% conversion cost from
  the less-attractive promise message. Net-negative; killed 2026-03-02.
- **[otp-mix-shift]** Blended on-time-to-promise rose +0.73pp Q1FY26→Q1FY27, but
  ship-to-home (majority-GMV, hardest channel) actually fell -0.20pp over the same
  window. The entire blended gain is attributable to pickup (BOPIS+curbside) mix
  share rising +8.0pp (driven by the Pickup Perks campaign, 2026-01-15) — pickup
  orders hit their promise ~99.6% of the time near-automatically.
- **[dc-automation-real-efficiency]** The same FON2/JOL1 DC automation rollout that
  confounds [wider-window-confound] also drove a genuine, durable cost-per-order
  improvement ($7.85 → $7.30 across the 6 quarters). Caveat: the single biggest QoQ
  drop (-$1.05, Q4FY26→Q1FY27) follows Q4FY26's own +$0.90 QoQ increase — the only
  increase in the series, ordinary peak/holiday cost pressure — so part of that drop
  is normal post-holiday reversion, not automation alone; the rollout window
  (2026-01-12 to 02-15) straddles both quarters and the two can't be fully separated
  at quarterly grain. Net of the Q4 peak spike, the full 6-quarter decline still
  supports a genuine, durable efficiency gain. Two different, real effects from one
  event — do not conflate "cost improved" with "on-time-rate improved for the same
  reason."
- **[voc-leads-quant]** Medallia "refund delay" verbatim share crossed 10% the week
  of 2025-12-15; the quantitative 4-week-rolling avg_refund_cycle_days didn't cross
  its 5.0-day SLA threshold until the week of 2026-01-05 (3 weeks later), and wasn't
  formally escalated until the 2026-02-02 MBR (7 weeks after VOC). Root cause:
  Ontario, CA returns center ~22% understaffed (hiring-freeze exception error).
- **[por-care-shared]** POR vertical's headline "avg refund cycle days" metric IS
  Care's refund-cycle-days series — same underlying fact, two org lenses. They must
  always match; a query treating them as independent will get confused by "two
  numbers for the same thing."
- **[care-deflection-quality-confound]** Care deflection rose 45.0%→49.6%→52.1%
  (Q4FY26→Q1FY27→Q2FY27 QTD), coinciding with the "Ask Acme v2" bot's rollout (since
  2025-09-15) — but the bot's own share of that rise is inferential, not
  holdback-proven: deflection was already climbing pre-bot (+2.3pp the prior
  quarter), and the single largest QoQ jump (+4.6pp) lands Q4FY26→Q1FY27, four-plus
  months after launch, not at launch. Separately, CSAT-among-deflected fell
  3.70→3.42 in the exact window the refund-delay ops problem was live, then
  partially recovered to 3.55. Rising deflection is directionally real progress AND
  was temporarily inflated by an unrelated ops failure; the two must be read
  together, not the rate alone.
- **[cltv-join-drop]** `member_cltv`'s canonical build LEFT JOINs `dim_member` to
  `fact_orders` with `COALESCE(trailing_12mo_gmv_usd, 0)`. An INNER JOIN silently
  drops the 20% of the 120,000-member panel (24,000 members) with zero orders in
  the trailing 12 months — inflating average CLTV from the correct $500/member to a
  wrong $625/member (25% overstatement) and hiding the dormant/churn-risk
  population entirely.
- **[benefit-adoption-cltv]** Members using 2+ Acme+ benefits renew at 95% vs. 71%
  for free-shipping-only members. The single strongest individual benefit is the
  streaming bundle (93% renewal alone) despite only 34% member awareness — the
  highest-leverage CLTV lever is a targeted awareness push, not a new benefit.
- **[marketplace-cannibalization]** Style GMV decelerated to +6.1% YoY in Q1FY27
  (vs. ~10% planned) while Resold accelerated to +90.9% YoY over the identical
  window, with Resold's apparel/style-adjacent category share rising 51%→62% YoY —
  a within-marketplace wallet-share shift, not a demand loss. Total Marketplace GMV
  is pacing at 117% of its FY27 goal. Invisible from the Style dashboard alone.
- **[assigned-vs-exposed]** `fact_experiment_exposures` carries both
  `units_assigned` and `units_exposed` so intent-to-treat vs. per-protocol analysis
  is checkable, not assumed. On Checkout Simplify, ~16% of assigned sessions were
  never exposed (client-side flag/cart-abandonment); the stated +2.1%/+0.8% readouts
  are already exposed-basis (per-protocol) — a naive assigned-basis (ITT)
  recomputation would understate them by roughly that fraction. Never compare an
  ITT-basis number from one experiment to a per-protocol number from another.
- **[flat-dataset]** BigQuery dataset is FLAT:
  `nexus-analyst-demo.acme_ecomm.<table>`. WRONG:
  `acme_ecomm.marts.membership.member_cltv`, `acme_ecomm.dbt_marts.*`. No nested
  datasets exist.
- **[sample-vs-population]** `dim_member` (120,000 rows), `dim_seller` (~2,500),
  `fact_orders` (~400,000), `fact_care_contacts` (~50,000), `fact_voc_responses`
  (~40,000), `fact_marketplace_listings` (~35,000), and `fact_membership_events`
  (~450,000) are representative panels/samples, NOT the full population.
  Company-level totals (14.62M members, $7.62B GMV run-rate, etc.) come from the
  aggregate marts or the Company section — never from `COUNT(*)`/`SUM()` on a panel
  table. See DO NOT REUSE / arithmetic convention 5.
- **[clhs-parked]** "Customer Lifetime Health Score" (CLHS) — a proposed composite
  membership-health score — is a PARKED/draft spec (owned by derek.holloway +
  renee.kowalski). No table, no columns exist. Current shipped proxy: `member_cltv`
  + benefit-adoption rate. Don't cite a CLHS score or band, it doesn't exist.
- **[aitable-jira-split]** Roadmap items opened before 2026-01-15 largely live in
  Aitable (legacy); items opened on/after that date live in Jira (consolidation
  project started 2026-01-15, not complete as of "today," 2026-07-20). Confluence
  holds PRDs for both eras. A query against only one ticketing system returns a
  partial roadmap.
- **[gmv-restatement]** Q4FY26 Marketplace GMV was flash-reported at $952.4M at
  quarter-close; restated to the canonical $975.0M in February 2026 after a
  returns-timing reclass. The "Compass" internal BI tool's cached view may still
  show the stale $952.4M figure to anyone who hasn't forced a refresh.
- **[offsetting-experiments]** Two in-flight US_CONV experiments started the
  same day (2026-06-08) and are both still running as of "today": "Search
  Relevance Re-ranking" (`exp_2601`, +1.6% conversion lift on its exposed arm)
  and "Item Page Media Carousel Autoplay" (`exp_2618`, -1.5% on its exposed
  arm — an intentionally well-meaning feature that backfired). Equal-weighted,
  their net effect on the topline dashboard is a ~+0.05% wash — invisible next
  to ordinary noise. Neither is the primary explanation for the Q2FY27
  WoW conversion drop (see the weekly US Conversion detail and
  [roadmap-doesnt-explain-it]); the point is that a PM checking "are any
  experiments live" and seeing a near-zero net figure could wrongly conclude
  *nothing* is running, when two individually meaningful, real, and opposite
  effects are — this is the "masked trend."
- **[item-page-metric-choice]** Two valid item-page metrics for the same
  quarter: view-to-cart rate (`add_to_cart_sessions/product_view_sessions`,
  18.0%→19.9% Q1FY27 pre/post cutover) and item-page-scoped conversion
  (`orders/product_view_sessions`, 5.13% Q1FY27) — deliberately different from
  standard site conversion (`orders/sessions`, 3.18%). Both metrics inherit
  the `sessions_definition_version` 1→2 cutover (2026-03-02) because they're
  built from the same `fact_traffic_daily` row as the site-wide rate — of
  view-to-cart's +1.9pp Q1FY27 raw move, ~+0.8pp is the same mechanical
  bump as the site-wide metric and ~+1.1pp is attributable to the Item Page
  Iteration Program's 6 shipped iterations. State which item-page metric and
  which version-basis you're using before answering "how did the item page
  do" — the two metrics and the two version-bases are 4 different
  legitimate-looking numbers for a question that sounds simple.
- **[roadmap-doesnt-explain-it]** For the Q2FY27 weekly US-conversion WoW drop
  (3.24%→2.86%, week of 07-11 vs. 07-18): the only marketing-calendar launch in
  that window ("Homepage Hero Banner Refresh," 2026-07-13) is homepage-only
  with no item-page/search overlap and no measurable conversion effect —
  ruled out by timing-proximity alone would be the trap. Of the -0.38pp move,
  -0.24pp is device-mix shift (app share 28.0%→37.6%) and -0.14pp is a real
  but modest web-conversion softening that is **not** explained by the shipped
  roadmap and **not** explained by the net effect of in-flight experiments
  (see [offsetting-experiments], which roughly cancel) — the honest answer
  says so plainly rather than forcing an attribution onto the residual.
- **[listing-accuracy-blind-spot]** Buyer-side Medallia theme
  `listing-accuracy-gap` (listings' photos/descriptions not matching true
  scale/condition/spec) sits at a non-trivial, roughly steady share in all
  four of Style (14%), Resold (12%), Collectibles (9%), and B2B (22%) — but
  none of the four verticals' current backlogs (see CROSS-VERTICAL BACKLOG
  SNAPSHOT, 20 enumerated items total) contains an initiative that owns it.
  Each vertical's PM sees only their own VOC report and their own backlog;
  the cross-vertical read is what's missing, not any one PM's diligence.
- **[seller-auth-friction]** The "Acme Verified"/GradeSure authentication
  requirement (launched 2025-09-08, badge shipped 100% 2025-11-20, itself
  proven worth +6.8% buyer-side conversion per the Verified Badge Prominence
  experiment) is a genuine two-sided tension: it took Collectibles' return
  rate from 11.2% (Q3FY26 peak) to 5.4% (Q2FY27) — a real buyer-trust win —
  while new-Collectibles-seller survival to their 10th listing (24%) runs well
  below Style (48%) and Resold (46%) in the same listing-count-based cohort,
  concentrated in the earliest listings (46% of Collectibles new sellers don't
  even reach listing 5, vs. 74-76% for Style/Resold). Sellers who get their
  debut listing GradeSure-verified within 7 days clear listing 10 at 2x the
  rate of those who don't (30% vs. 15%). Removing the requirement isn't free
  (it would undo the return-rate win); the tension is real on both sides and
  should be surfaced as a trade-off, not resolved by assumption.

---

## DISTRACTORS — fine as NOISE (must be self-correcting or clearly stale, never asserted as truth)

- Compass dashboard PDT still showing Q4FY26 Marketplace GMV as $952.4M — corrected
  by the canonical $975.0M in the mart (see [gmv-restatement]).
- A flash Q1FY27 US conversion estimate of ~2.96% (computed on pre-fix,
  `sessions_definition_version=1`-only partial data before the full quarter
  reprocessed) floating around early in the quarter, vs. the final blended 3.18%.
- Someone querying `acme_ecomm.marts.membership.member_cltv` (nested-looking path)
  and getting corrected — flat path is `acme_ecomm.member_cltv`.
- "Customer Lifetime Health Score" (CLHS) cited as if live — corrected to
  parked/draft, no such table (see [clhs-parked]).
- The abandoned "Style Conversion Recovery Plan" draft (Confluence, undated,
  circa Q1FY27) recommending Trust & Safety headcount move off Collectibles onto
  Style — superseded/never actioned once [marketplace-cannibalization] showed the
  Style dip wasn't a Style-specific problem. Fine to include as a draft that
  circulated and was set aside — never as an implemented decision.
- Someone citing the Checkout Simplify full-window "+2.1%" as the checkout
  redesign's clean causal effect — corrected by [checkout-confound] to the
  pre-confound +0.8%.
- The "Homepage Hero Banner Refresh" launch (2026-07-13) coinciding with the
  Q2FY27 WoW conversion dip — same-week timing invites a causal read the data
  doesn't support (homepage-only, no item-page/search overlap, no measurable
  effect); see SIGNAL [roadmap-doesnt-explain-it].
- Off-topic chatter: standup scheduling, PTO, office logistics, unrelated tooling
  migrations (a Looker-to-Compass-analog dashboard migration is fine background
  noise), team lunch, holiday party planning. Lots of this is GOOD — more noise.

---

## ORG / PEOPLE (handle → name, role, team, assoc_id) — reuse these exactly

**Leadership**
- deborah.osei → Deborah Osei, CEO Acme eCommerce, Executive, assoc_100001
- felix.arroyo → Felix Arroyo, SVP Product & Growth, Product, assoc_100010
- hannah.brennan → Hannah Brennan, SVP Customer Care, Care, assoc_100020
- victor.okonkwo → Victor Okonkwo, SVP Marketplace, Marketplace, assoc_100030
- renee.kowalski → Renee Kowalski, SVP Membership (Acme+), Membership, assoc_100040
- ben.tanaka → Ben Tanaka, SVP Supply Chain & Fulfillment, Fulfillment, assoc_100050
- carlos.figueroa → Carlos Figueroa, VP Data & Analytics, Data, assoc_100060
- nadia.esposito → Nadia Esposito, Head of Product Operations, Product Ops, assoc_100070

**Vertical PMs**
- maya.lindqvist → Maya Lindqvist, Director PM US Conversion & Traffic (incl.
  View Item Page surface, US_CONV — owns the Item Page Iteration Program),
  Product, assoc_100110
- owen.faust → Owen Faust, Sr PM Checkout & Conversion (incl. Search surface,
  US_CONV), Product, assoc_100111
- sanjay.bhatt → Sanjay Bhatt, Sr PM Marketplace Collectibles (View Item Page
  surface, Collectibles), Marketplace, assoc_100120
- ines.delgado → Ines Delgado, Sr PM Marketplace Style (View Item Page surface,
  Style), Marketplace, assoc_100121
- noah.kessler → Noah Kessler, Sr PM Marketplace Resold (View Item Page
  surface, Resold), Marketplace, assoc_100122
- camille.duarte → Camille Duarte, Sr PM Marketplace Seller Experience —
  Seller Listing + Seller Optimization surfaces, all 3 Marketplace
  sub-verticals, Marketplace, assoc_100123 (joined 2026-04-08)
- aisha.rahman → Aisha Rahman, Director PM Care (Automate/Avoid), Care, assoc_100130
- julian.moss → Julian Moss, Sr PM Care (Optimize/Platform), Care, assoc_100131
- tara.oduya → Tara Oduya, Director PM Speed & Fulfillment, Fulfillment, assoc_100140
- leo.brandt → Leo Brandt, Sr PM Delivery Promise, Fulfillment, assoc_100141
- simone.laurent → Simone Laurent, Director PM Membership (Acme+), Membership, assoc_100150
- derek.holloway → Derek Holloway, Sr PM Membership Benefits & CLTV, Membership, assoc_100151
- malik.hendon → Malik Hendon, Sr PM Acme Business (B2B/Wholesale) — B2B's
  first dedicated PM, B2B, assoc_100160 (hired 2025-06-15)

**Surface ownership** (the named surfaces the customer's PMs organize around
— resolves "who should own it" questions; a blank cell is a genuine gap, not
an omission):

| Surface | US_CONV | Style | Resold | Collectibles | B2B |
|---|---|---|---|---|---|
| View Item Page | maya.lindqvist | ines.delgado | noah.kessler | sanjay.bhatt | — (no consumer item page) |
| Search | owen.faust | victor.okonkwo (SVP-level; no dedicated Marketplace-wide search PM — a real gap) | " | " | — |
| Seller Listing | n/a (no sellers) | camille.duarte | camille.duarte | camille.duarte | n/a |
| Seller Optimization | n/a | camille.duarte | camille.duarte | camille.duarte | n/a |

**Data & Analytics**
- wei.hartono → Wei Hartono, Analytics Engineer (owns core marts), Data, assoc_100210
- amara.shah → Amara Shah, Data Analyst (Finance/MBR), Data, assoc_100211
- connor.blake → Connor Blake, Data Engineer (pipeline/freshness), Data, assoc_100212
- giulia.romano → Giulia Romano, Analytics Engineer (Care & VOC/Medallia), Data, assoc_100213

**Ops leads**
- dominic.paquet → Dominic Paquet, Care Ops Lead (bot/deflection), Care, assoc_100310
- lucia.ferreira → Lucia Ferreira, Trust & Safety Lead (Marketplace), Marketplace, assoc_100320
- gabriel.stroud → Gabriel Stroud, Fulfillment Ops Lead (DC network), Fulfillment, assoc_100330

**External**
- ronnie.aldridge → external, owner/operator of Northfield Apparel Co. (sel_500034) — NOT an Acme associate.

---

## CANONICAL SELLERS — already exist in the corpus; use ONLY these facts

- sel_500012 Timeworn Treasures — Collectibles, top-tier; GMV grew ~8x across the 6
  quarters riding the boom + early Verified-Badge adoption; #1 Collectibles seller
  by Q2FY27 GMV.
- sel_500034 Northfield Apparel Co. — Style, mid-tier (owned by ronnie.aldridge);
  wrongly named in the abandoned "Style Conversion Recovery Plan" draft as a
  representative "declining" seller — GMV actually flat/stable, not declining.
- sel_500061 Loop Resale Collective — Resold, fast-growing; GMV roughly doubled
  across the 6 quarters, a poster child for the recommerce acceleration.
- sel_500089 Bramblewood Vintage — Collectibles; 3 counterfeit-listing violations
  flagged 2025-08-12, suspended 2025-09-02, reinstated 2026-01-15 post-compliance-
  review.
- sel_500103 Kestrel & Vine — Style, large; the specific account named in the Q1FY27
  Style headcount ask.
- sel_500147 Harlow & Finch — Resold, mid-tier; steady, uneventful — nothing
  noteworthy happened here across all 6 quarters (deliberate contrast entry).

## CANONICAL MEMBER ARCHETYPES — first-name only + member_id, reuse exactly

- mem_1000042 "Dana" — power benefit-user (free shipping + early access +
  Reelstream), 4-year tenure, renews every year, high CLTV.
- mem_1000178 "Marisol" — dormant (paying annual plan, zero orders trailing 12
  months) — the poster child for [cltv-join-drop].
- mem_1000390 "Jamal" — churn-risk: 2 open P1 care contacts, an NPS detractor
  response last quarter.
- mem_1000512 "Grethe" — was unaware of the streaming benefit; churned after two
  late ship-to-home deliveries in one quarter.
- mem_1000640 "Oskar" — signed up via the Fall Savings promo (2025-09-20), now a
  2-benefit adopter (early access + free shipping), renews reliably.

## CANONICAL NEW-SELLER ARCHETYPES (funnel cohort) — first-name-optional + seller_id, reuse exactly

- sel_500241 — Collectibles, onboarded 2025-11 (`application_date` 2025-11-03,
  `onboarded_date` 2025-11-10); debut listing not GradeSure-verified within 7
  days (the "not verified within 7 days" bucket); churned after 3 listings,
  never reached listing 5 — the poster child for [seller-auth-friction].
- sel_500242 — Collectibles, onboarded 2025-10 (`application_date` 2025-10-02,
  `onboarded_date` 2025-10-08); debut listing GradeSure-verified within 4 days
  (the "verified within 7 days" bucket); reached listing 10 by Q1FY27 and is
  "sustained" — the contrast case showing the friction is survivable when
  verification happens fast.
- sel_500243 — Style, onboarded 2025-12 (`application_date` 2025-12-01,
  `onboarded_date` 2025-12-05); no authentication requirement in Style;
  reached listing 10 within 10 weeks with no unusual friction — the
  cross-category contrast that isolates Collectibles' authentication
  requirement (not "being a new seller" generally) as the driver.

## DO NOT REUSE — forbidden names/handles/IDs (all belong to the SaaS Acme Inc)

**Never reuse these person handles/names** (from `datasets/acme/CANON.md`): sam.reyes,
priya.anand, marcus.webb, jordan.hayes, elena.volkov, dan.lee, rachel.stein,
jasmine.park, tomás.vega, anika.schmidt, lina.cho, rajiv.menon, david.kim,
nina.patel, marco.silva, olivia.tran, grace.liu, tom.becker, sarah.chen, yuki.sato,
omar.haddad, jorge.martinez, theo.novak — and any Faker-generated employee name that
happens to already appear in the SaaS corpus.

**Never reuse these ID prefixes** — they belong to the SaaS warehouse:
`cust_`, `user_`, `emp_`, `sub_`, `inv_`, `wf_`, `wfr_`, `evt_`, `tkt_`, `opp_`,
`nps_`, `tch_`. This eCommerce corpus uses an entirely disjoint prefix set:
`mem_`, `assoc_`, `sel_`, `lst_`, `ord_`, `case_`, `voc_`, `svoc_` (seller VOC —
deliberately distinct from buyer VOC's `voc_`), `camp_`, `exp_`, `sku_`,
`fc_`/`str_` (node ids). **Never reuse these specific pinned SaaS customer IDs**
(forbidden literal strings, even though prefixes already differ): cust_000087,
cust_000089, cust_000156, cust_000212, cust_000214, cust_000219, cust_000223,
cust_000281, cust_000287, cust_000301, cust_000412, cust_000477, cust_000509,
cust_000512, cust_000601, cust_000621, and cust_000700 through cust_000714.

**Company naming**: "Acme Inc" is reserved for the B2B SaaS. This company is always
just **"Acme"** in prose, `acme-ecomm` in filenames/config, `acme_ecomm` in BigQuery
identifiers. Never write "Acme Inc" in this corpus.

## Seller ID ranges

Pinned canonical: sel_500012, 500034, 500061, 500089, 500103, 500147. Shared cast:
sel_500200–500213 (below). New-seller archetypes (funnel cohort, pinned):
sel_500241–500243 (below). New one-off sellers: use sel_500244–500999 (avoid
500012–500243 entirely — it's reserved).

## SHARED CAST — recurring NEW noise sellers. Reuse these EXACT attributes.

(id | seller | category | GMV tier | onboarded | status | fulfillment_method | home_country)

- sel_500200 | Silverline Card Co. | collectibles | mid | 2024-08-12 | active | seller_fulfilled | US
- sel_500201 | Heirloom & Co. | collectibles | small | 2025-02-03 | active | ship_with_acme | US
- sel_500202 | Rustbelt Relics | collectibles | small | 2025-09-20 | active | seller_fulfilled | US
- sel_500203 | Marrow Lane Vintage | resold | mid | 2024-11-05 | active | seller_fulfilled | US
- sel_500204 | ReWear Collective | resold | large | 2024-05-14 | active | ship_with_acme | US
- sel_500205 | Thriftline Goods | resold | small | 2025-06-01 | active | seller_fulfilled | CA
- sel_500206 | Second Cycle Supply | resold | mid | 2025-03-22 | active | seller_fulfilled | US
- sel_500207 | Cascade Denim Works | style | large | 2024-02-18 | active | ship_with_acme | US
- sel_500208 | Meridian Threads | style | mid | 2024-09-09 | active | seller_fulfilled | US
- sel_500209 | Palisade Footwear | style | mid | 2025-01-11 | active | ship_with_acme | MX
- sel_500210 | Amberlyn Studio | style | small | 2025-07-30 | active | seller_fulfilled | US
- sel_500211 | Coastal Trading Post | other (home goods) | small | 2024-12-01 | active | seller_fulfilled | US
- sel_500212 | Fernwood Outdoors | other (outdoor gear) | mid | 2025-04-17 | suspended (2026-02, listing-quality review) | seller_fulfilled | US
- sel_500213 | Basalt & Bloom | style | small | 2025-10-05 | active | ship_with_acme | CA

If you need extra one-off sellers beyond the cast, invent NEW names and use IDs in
sel_500240–500999 (avoid the reserved 500012–500239 range).

---

## STYLE

- Match the voice of the existing file type (read the examples you're given).
  YAML frontmatter at top: `title`, `source_url` (`internal://acme-ecomm/...`),
  `license: synthetic-demo`, `attribution`, `fetched_at`, `adapter`.
- Adapters, mapped to the customer's named systems: `bq_query_log` /
  `hive_query_log` (BigQuery, Hive), `fullstory_session_note` (FullStory —
  referenced qualitatively in docs; not a BQ table), `expo_experiment` (dim_experiment
  + readouts), `marketing_calendar_export`, `mbr_deck_notes` (MBR/business data),
  `medallia_verbatim` (buyer VOC), `seller_pulse_survey` (seller VOC,
  `fact_seller_voc_responses` — separate from `medallia_verbatim`, never mix
  the two), `aitable_card`, `jira_ticket`, `confluence_page`
  (strategy/execution/roadmap), `slack_thread`, `postmortem`, `meeting_notes`,
  `org_announcement`.
- Realistic, messy, human. Heavy noise is GOOD. Bury ~1 signal per several hundred
  lines; the rest is plausible chatter/queries/rows/tickets.
- Dates 2025–2026, consistent with the 6-quarter window (2025-02-01 through
  2026-07-20). Money/GMV/seats must match the numbers tables above whenever a
  specific quarter or entity is named.
- Documents are generated in **chronological rounds**; a document dated later than
  an event in the timeline may reference it as settled history ("the checkout
  experiment Owen shipped back in April," "since the Ontario staffing mess got
  fixed"); a document dated before an event must not foreshadow it.
