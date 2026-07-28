# ACME CANON — authoritative fact sheet for source authoring

You are writing ONE synthetic internal source file for "Acme Inc", a fictitious B2B SaaS.
Everything below is CANON. Never contradict it. Bury the SIGNALS (correct facts) inside
heavy, realistic NOISE. Reuse the shared CAST so every file references the SAME entities
with the SAME attributes. This is synthetic demo data (disclaimer in every frontmatter).

## Company
- Workflow-automation platform (connect SaaS tools, run on schedule/webhook/on-demand). Think Zapier / Make / Tray, priced for teams >50 seats.
- Founded Jan 2023. HQ San Francisco; EMEA office Amsterdam. Series B, $80M raised total (last round Q3 2025).
- ~100 employees: Eng ~30, Sales ~20, CS ~15, Marketing ~10, Product/Design ~15, Finance/Ops/People/Legal ~10.
- 800 customers in dim_customers (~745 active, ~45 churned, ~10 paused). ~24,000 users provisioned, ~16,000 active in last 28d.
- ARR ~$39M: Business ~$32M / Enterprise ~$6M / Pro ~$1M. Free ARR = $0.
- Plan mix among active paying: Pro ~38%, Business ~27%, Enterprise ~5%, Free (non-paying) ~30%.
- Data range 2023-01-01..2026-04-30. dbt refresh daily; BI warehouse lags prod ~2h. Snapshot "today" ~2026-05-04.

## Plans (dim_plans)
| Tier | Price | Min seats | Quota |
|---|---|---|---|
| Free | $0 | 1 | 100 runs/mo, 2 active workflows |
| Pro | $49/seat/mo | 1 | 10K runs/mo, unlimited workflows |
| Business | $149/seat/mo | 50 | 100K runs/mo, SSO, audit log, priority support |
| Enterprise | Custom, $50K–$500K ACV | 250 | Unlimited runs, dedicated CSM, SOC2, custom SLA |
PLG: Free→Pro self-serve; Pro→Business and Business→Enterprise are AE-led. account_tier ∈ {SMB, MM, Ent}. Enterprise sales cycle ~90 days.

## Warehouse — `nexus-analyst-demo.acme` (BigQuery, FLAT — see SIGNAL flat)
Base tables (5 dims + 8 facts):
- dim_customers(customer_id, company_name, signup_date, country, region, industry, account_tier, current_plan_tier, current_mrr_usd, seat_count_licensed, status, churn_date, csm_employee_id, ae_employee_id, acquisition_channel)
- dim_users(user_id, customer_id, email_domain, role, signup_date, last_login_date, is_active, invited_by_user_id)
- dim_employees(employee_id, full_name, team, role, manager_employee_id, hire_date, termination_date, location, is_active)
- dim_plans(plan_tier, monthly_price_per_seat_usd, min_seats, workflow_run_quota_per_month, storage_gb, sla_uptime_pct)
- dim_dates(date, year, quarter, month, month_name, week, day_of_week, is_weekend, is_business_day)
- fact_subscriptions(subscription_id, customer_id, plan_tier, start_date, end_date, mrr_usd, seat_count, billing_cycle, is_current, change_type, changed_from_subscription_id)
- fact_invoices(invoice_id, customer_id, subscription_id, invoice_date, period_start, period_end, amount_usd, status, paid_at)
- fact_workflow_runs(run_id, workflow_id, customer_id, triggered_at, triggered_by, status, duration_ms, step_count, error_code)
- fact_user_events(event_id, user_id, customer_id, event_at, event_name, properties_json)
- fact_support_tickets(ticket_id, customer_id, user_id, opened_at, closed_at, channel, priority, category, resolution_time_hours, csat_score, assigned_to_employee_id)
- fact_opportunities(opportunity_id, customer_id, account_name, ae_employee_id, sdr_employee_id, created_date, stage, amount_usd, close_date, closed_won_at, loss_reason)
- fact_nps_responses(response_id, customer_id, user_id, responded_at, score, comment, segment, survey_quarter)
- fact_marketing_touches(touch_id, lead_email_hash, customer_id, touched_at, channel, campaign, utm_source, utm_medium, utm_campaign, attributed_revenue_usd)
Materialized marts (also flat under acme):
- arr_snapshot(snapshot_date, arr_usd, arr_pro_usd, arr_business_usd, arr_enterprise_usd, paying_customers)
- nrr_trailing_12(cohort_size, cohort_start_mrr_usd, cohort_end_mrr_usd, nrr, grr, churned_mrr_loss_usd, expansion_mrr_usd)
- account_health(customer_id, account_tier, current_plan_tier, has_uncollectible_recent, n_open_p1_over_48h, has_open_p1_over_48h, has_recent_nps_detractor, is_engaged, utilization_band, account_health_status)
- bookings_attribution(opportunity_id, customer_id, account_name, bookings_acv_usd, closed_won_at, first_touch_channel)
- workflow_runs_daily(run_date, customer_id, n_runs, n_success, success_rate, p50_duration_ms, p95_duration_ms, p99_duration_ms, auth_failed_count, rate_limited_count, step_timeout_count, integration_down_count)
error_code values: AUTH_FAILED, RATE_LIMITED, STEP_TIMEOUT, INTEGRATION_DOWN, SCHEMA_MISMATCH, NULL_PAYLOAD (or empty on success).
acquisition_channel / first_touch_channel ∈ {organic, paid_search, outbound, content, referral, partner, event, inbound}.

## SIGNALS — correct buried truths (state them VERBATIM-accurate; scatter through noise)
- [arr] ARR = SUM(mrr_usd)*12 over fact_subscriptions where is_current AND plan_tier!='Free'. arr_snapshot is canonical for board; do NOT re-derive off dim_customers.current_mrr_usd (drifts intraday). ~$39M (Biz ~$32M / Ent ~$6M / Pro ~$1M).
- [nrr] nrr_trailing_12 is canonical board NRR. Fixed cohort = paid (non-Free) customers as of snapshot_date−12mo. Churned customers STAY in the cohort at $0 end MRR — LEFT JOIN + COALESCE(end_mrr_usd,0). An INNER JOIN drops churned and INFLATES NRR. NRR ~1.07, GRR ~0.94 (GRR caps numerator at denominator, no expansion credit). Downgrades to Free count as churn.
- [bookings] bookings_acv_usd is ALREADY annualized — do NOT multiply by 12. Free→Paid self-serve conversions do NOT appear in bookings_attribution (opportunity-sourced AE-led deals only). Q1-bookings-by-channel = group bookings_attribution by first_touch_channel.
- [flat] BigQuery dataset is FLAT. Correct: `acme.account_health`. WRONG: `acme.marts.cs.account_health`, `acme.dbt_marts.*`, `acme.marts.finance.*`. dbt folder layout (marts/finance, marts/cs) is filesystem-only, NOT a table path. No nested datasets.
- [engaged] Engaged customer = ≥3 active users AND ≥10 successful workflow runs in trailing 28 days. Recalibrated in 2025-Q4 (previously looser). account_health.is_engaged uses the same window; 'monitoring' = not engaged.
- [health] account_health_status enum: critical / at_risk / monitoring / stable / healthy_expansion. Critical rule differs by tier: Enterprise critical ONLY on a recent uncollectible invoice (no utilization rule — unlimited seats). Non-Enterprise critical on uncollectible OR utilization_band < 0.20. at_risk = open P1 >48h OR recent NPS detractor. healthy_expansion = engaged AND utilization ≥ 0.6. utilization_band = NULL for Enterprise else active_users_28d/seat_count_licensed.
- [vrs] The Value Realization Score (VRS) is a PARKED draft spec — `vrs_band` and `champion_login_recency` columns are NOT built. Use account_health as the shipped proxy. Don't query VRS, it doesn't exist.
- [plans] (prices above). [misc] no step-level facts in BI; BI lags prod ~2h.

## DISTRACTORS — fine to include as NOISE (must be self-correcting or clearly stale/wrong, never asserted as truth)
- Someone querying `acme.marts.cs.account_health` and getting corrected (path doesn't exist).
- "ARR $42M" floating around = stale Looker PDT before the cache fix; real ~$39M.
- A draft suggesting `bookings_acv_usd*12` → corrected (already annual).
- Off-topic chatter: lunch/coffee debates, office logistics, standup-time polls, unrelated Linear/Looker migrations, weekend plans. Lots of this is GOOD (more noise).

## ORG / PEOPLE (handle → name, role, employee_id) — reuse these exactly
- sam.reyes → Sam Reyes, CEO, emp_001
- priya.anand → Priya Anand, VP Eng, emp_010
- marcus.webb → Marcus Webb, VP Sales, emp_020
- elena.volkov → Elena Volkov, VP Customer Success, emp_040
- dan.lee → Dan Lee, VP Product, emp_050
- rachel.stein → Rachel Stein, CFO, emp_060
- jasmine.park → Jasmine Park, VP Marketing, emp_070
- lina.cho → Lina Cho, Finance/Data Analyst (owns finance marts), emp_062
- rajiv.menon → Rajiv Menon, Analytics Engineer (owns dbt), emp_012
- david.kim → David Kim, Data Engineer, emp_013
- nina.patel → Nina Patel, Analytics Engineer, emp_014
- marco.silva → Marco Silva, CSM, emp_041
- olivia.tran → Olivia Tran, CSM, emp_042
- grace.liu → Grace Liu, CSM, emp_043
- tom.becker → Tom Becker, AE, emp_021
- sarah.chen → Sarah Chen, AE, emp_023
- yuki.sato → Yuki Sato, AE, emp_024
- omar.haddad → Omar Haddad, AE, emp_026
- jorge.martinez → Jorge Martinez, RevOps (running CRM migration), emp_063
- theo.novak → external customer-side champion (NOT an Acme employee)

## CANONICAL CUSTOMERS — already exist in the corpus; use ONLY these facts, do not invent contradicting specifics
- cust_000287 Beacon Studios — Business, 65 seats, $9,685 MRR (~$116K ARR), churned 2026-02-18, procurement/parent-company driven (NOT product dissatisfaction). Healthy engagement/NPS at time of churn.
- cust_000412 Drag Industries — Enterprise prospect/customer, multi-stakeholder POC + QBR + FY26 renewal storyline.
- cust_000509 — Enterprise POC storyline.
- cust_000601 Nimbus Finance — mid-market/discovery storyline.
- cust_000089 Greenfield SaaS — discovery storyline.
- cust_000156 — budget-cut churn storyline.
Reference these by name where natural, but ONLY with the facts above.

## DO NOT REUSE these existing customer IDs for NEW invented customers (they're already pinned):
cust_000087, cust_000089, cust_000156, cust_000212, cust_000214, cust_000219, cust_000223, cust_000281, cust_000287, cust_000301, cust_000412, cust_000477, cust_000509, cust_000512, cust_000601, cust_000621

## SHARED CAST — recurring NEW noise customers. Reuse these EXACT attributes everywhere they appear.
(id | company | tier | seats | mrr_usd | region | industry | channel | status | csm | ae)
- cust_000700 | Cobalt Systems   | Business   | 80  | 11,920 | EMEA    | fintech    | outbound    | active            | marco.silva  | tom.becker
- cust_000701 | Marigold Health  | Enterprise | 300 | 15,000 | NA-East | healthtech | partner     | active            | olivia.tran  | sarah.chen
- cust_000702 | Driftwood Media  | Pro        | 18  | 882    | NA-West | media      | organic     | active            | grace.liu    | yuki.sato
- cust_000703 | Yarrow Logistics | Business   | 120 | 17,880 | APAC    | logistics  | event       | active            | marco.silva  | omar.haddad
- cust_000704 | Onyx Robotics    | Enterprise | 500 | 35,000 | NA-West | devtools   | outbound    | active            | olivia.tran  | tom.becker
- cust_000705 | Pebble Digital   | Pro        | 6   | 294    | EMEA    | martech    | content     | active            | grace.liu    | sarah.chen
- cust_000706 | Tamarind Group   | Business   | 55  | 8,195  | NA-East | insurance  | referral    | paused (2026-01)  | marco.silva  | sarah.chen
- cust_000707 | Verdant Cloud    | Enterprise | 260 | 8,000  | APAC    | ecommerce  | inbound     | active            | olivia.tran  | omar.haddad
- cust_000708 | Kestrel Networks | Business   | 70  | 10,430 | NA-West | devtools   | outbound    | churned (2025-11, budget) | marco.silva | tom.becker
- cust_000709 | Willow Works     | Pro        | 25  | 1,225  | LATAM   | gaming     | organic     | active            | grace.liu    | yuki.sato
- cust_000710 | Sable Analytics  | Business   | 90  | 13,410 | EMEA    | fintech    | partner     | active            | marco.silva  | sarah.chen
- cust_000711 | Ember Industries | Enterprise | 350 | 25,000 | NA-East | logistics  | outbound    | active            | olivia.tran  | tom.becker
- cust_000712 | Juniper Collective | Pro      | 12  | 588    | NA-West | media      | content     | churned (2026-01, product fit) | grace.liu | yuki.sato
- cust_000713 | Harbor Dynamics  | Business   | 150 | 22,350 | APAC    | insurance  | event       | active            | marco.silva  | omar.haddad
- cust_000714 | Quartz Foundry   | Enterprise | 280 | 12,000 | EMEA    | healthtech | partner     | active            | olivia.tran  | sarah.chen
(MRR math: Pro $49/seat, Business $149/seat, Enterprise = ACV/12. All consistent.)
If you need extra one-off customers beyond the cast, invent NEW names and use IDs in cust_000720..cust_000799 (avoid the pinned list above).

## STYLE
- Match the voice of the existing file type (read the examples you're given). Frontmatter YAML at top: title, source_url (internal://acme/...), license: synthetic-demo, attribution, fetched_at, adapter.
- Realistic, messy, human. Heavy noise is GOOD. Bury ~1 signal per several hundred lines; the rest is plausible chatter/queries/rows.
- Dates 2025–2026 mostly. Money/seats/tiers must match the cast/plan math when you name a specific customer.
