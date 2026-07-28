---
title: "Slack #marketing-analytics channel archive — 2025-2026"
source_url: "internal://acme/slack-marketing-analytics-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #marketing-analytics

**Jan 6, 2025**

**jasmine.park** 09:12 AM
Happy New Year team! :sparkles: Let’s hit the ground running. @alex.wright @maya.chen — I need a final cut of the 2024 channel performance. Rachel wants to see the split of bookings by `first_touch_channel` for the Q4 board deck by Wednesday.

**alex.wright** 09:15 AM
On it, Jasmine. I’m pulling from `nexus-analyst-demo.acme.bookings_attribution`. Just to confirm, we’re sticking with First Touch for the board slides? I know we talked about moving to a linear multi-touch model.

**jasmine.park** 09:17 AM
Stick with First Touch for the "Acquisition Source" slide to keep it consistent with the Q1-Q3 reports. We can add a footnote about the multi-touch pilot.

**lina.cho** 10:45 AM
@alex.wright Quick heads up when you run that—make sure you're looking at `bookings_acv_usd`. And remember, that field is *already annualized*. I saw a draft last month where someone multiplied it by 12 and almost gave Rachel a heart attack thinking we’d tripled our Enterprise pipeline overnight.

**maya.chen** 11:02 AM
Lol, thanks Lina. Yeah, we learned that lesson the hard way.
Also, quick question for @jorge.martinez — I’m seeing some `null` values in `first_touch_channel` for deals that closed in late December. Did something break in the CRM sync?

**jorge.martinez** 11:15 AM
Ugh, probably. We had a workflow rule in the CRM that was overwriting the `Lead Source` field if a contact was re-added via a webinar upload. I’m cleaning it up now. It should be reflected in the BigQuery sync by the 2pm refresh.

---

**Jan 15, 2025**

**marcus.webb** 02:20 PM
Hey team, we’re seeing a ton of "organic" leads coming in that look suspiciously like they should be "outbound". For example, Cobalt Systems (cust_000700) shows up as organic in the dashboard, but Tom Becker has been hitting them up for three months.

**alex.wright** 02:25 PM
Checking... Okay, looking at `nexus-analyst-demo.acme.fact_marketing_touches`. It looks like the first recorded touch for Cobalt Systems was a direct site visit on Jan 4. If Tom was emailing them, did he use a tracked link?

**tom.becker** 02:30 PM
I sent them the standard one-pager PDF. It doesn't have UTMs.

**maya.chen** 02:35 PM
That’s why. If they click a link in a plain email or just type `acme.com` into their browser, it defaults to `organic` or `direct`. We really need the AEs to use the personalized outreach links from the Sales Loft sequences.

**marcus.webb** 02:40 PM
Understood. But for the pipeline report, can we manually override those? My team is getting 60% of the pipeline credit but only 30% of the "closed-won" credit because the attribution is stripping away the outbound source.

**jasmine.park** 03:00 PM
Marcus, we can't manually override the warehouse data for every deal, but Alex, can we look at a "Sourced by SDR/AE" view vs "Marketing Touched" view for the Sales QBR?

---

**Feb 3, 2025**

**jorge.martinez** 09:00 AM
**@channel IMPORTANT:** Starting the CRM migration to the new schema today. Data in `nexus-analyst-demo.acme.fact_marketing_touches` might be stale for the next 48-72 hours while we re-map the objects.

**lina.cho** 09:15 AM
@jorge.martinez will this affect the `arr_snapshot`? I have to pull the Jan month-end numbers for Finance.

**jorge.martinez** 09:20 AM
No, `arr_snapshot` and `fact_subscriptions` are safe. Those pull from the billing system (Stripe/Internal DB). It’s only the attribution and opportunity-level marketing data that's moving.

**alex.wright** 11:30 AM
Is this why I'm seeing 0 spend for `paid_search` today?

**maya.chen** 11:32 AM
No, that's because I paused the Google Ads campaigns while we fix the landing page for the "Workflow Automation for Fintech" campaign. The conversion rate was tanking.

---

**Feb 14, 2025**

**yuki.sato** 04:10 PM
Happy Valentine's Day! Can someone check why Driftwood Media (cust_000702) isn't showing up in my "Bookings" dashboard? They signed their Pro plan yesterday.

**alex.wright** 04:15 PM
Hey Yuki, looking at the logs... Driftwood Media is on a Pro plan ($882/mo). They signed up via the self-serve flow, right?

**yuki.sato** 04:16 PM
Yeah, they used the website.

**alex.wright** 04:20 PM
That’s the reason. Self-serve Free-to-paid conversions don’t show up in `bookings_attribution`. That table only tracks opportunity-sourced, AE-led deals (usually Business or Enterprise). For PLG conversions, you need to check `nexus-analyst-demo.acme.fact_subscriptions`.

**yuki.sato** 04:22 PM
Ah, okay. That's confusing. Why don't we have one view for all revenue?

**lina.cho** 04:30 PM
Because the board wants to see "New Business Bookings" (AE-led) separately from "Self-Serve/Expansion" (PLG). If we mix them, it's harder to calculate Sales CAC.

---

**Mar 12, 2025**

**jasmine.park** 10:00 AM
Alex, can we get a ROAS analysis for the LinkedIn spend in Feb? We spent about $45k.

**alex.wright** 11:45 AM
Sure thing.
Feb LinkedIn Spend: $45,200
Attributed Bookings (First Touch): $112,000 (3 Enterprise deals, including Marigold Health - cust_000701)
ROAS: ~2.48x
If we look at Multi-Touch, it jumps to about 3.1x because LinkedIn is often the 2nd or 3rd touch for our content pieces.

**jasmine.park** 11:50 AM
2.48x is a bit lower than our target of 4.0x. What happened?

**maya.chen** 11:55 AM
A lot of the spend went into the "Scaling with Security" whitepaper. It drove a ton of leads (500+), but most were lower-level managers at SMBs, not the Enterprise decision-makers we wanted.

**marcus.webb** 12:05 PM
Yeah, my guys said those leads were "junk". Lots of students and consultants looking for free info.

**jasmine.park** 12:10 PM
Let’s pivot the Q2 spend toward the "Executive Automation" webinar series. Higher intent.

---

**Apr 22, 2025**

**maya.chen** 09:30 AM
Who changed the `utm_campaign` on the Spring Webinar landing page? It was `spring-automation-2025` but now I’m seeing `webinar-q2-promo` in the latest batch of leads.

**jorge.martinez** 09:45 AM
That might have been the contractor we hired for the SEO audit. They were "standardizing" the tags.

**maya.chen** 09:47 AM
Standardizing? It broke the tracking for my dashboard. Now I have to update the regex in my SQL query to catch both strings.

**alex.wright** 10:00 AM
@maya.chen just use a `CASE` statement in the `nexus-analyst-demo.acme.fact_marketing_touches` view for now.

```sql
SELECT
  touch_id,
  CASE
    WHEN utm_campaign IN ('spring-automation-2025', 'webinar-q2-promo') THEN 'Spring Webinar 2025'
    ELSE utm_campaign
  END as campaign_unified
FROM nexus-analyst-demo.acme.fact_marketing_touches
```

**maya.chen** 10:05 AM
Thanks Alex. Still annoying.

---

**May 19, 2025**

**jasmine.park** 02:00 PM
Quick check — what’s our current ARR? I’m seeing $38.5M in one Looker tile and $41.2M in another.

**lina.cho** 02:15 PM
The $41.2M is likely a stale PDT or it’s pulling from `dim_customers.current_mrr_usd`, which can drift if the sync hasn't finished.
The source of truth is `nexus-analyst-demo.acme.arr_snapshot`.
As of this morning, we are at ~$39.1M total ARR.
Breakdown:
- Business: ~$32M
- Enterprise: ~$6.1M
- Pro: ~$1M

**jasmine.park** 02:20 PM
Got it. $39M. I’ll use that for the internal monthly update.

---

**Jun 10, 2025**

**sarah.chen** 11:00 AM
Hey, looking at Tamarind Group (cust_000706). They’re listed as "referral" in my CRM view, but I know for a fact they came in via the Dutch Partner program.

**alex.wright** 11:15 AM
Checking `fact_marketing_touches`...
Looks like they clicked a referral link from a blog post *before* the partner officially registered the lead. First touch wins in the current model.

**sarah.chen** 11:20 AM
That’s going to mess with the partner payout. Can we adjust?

**jorge.martinez** 11:25 AM
I'll talk to the partner manager. We might need to implement a "Partner Override" flag in `dim_customers`.

---

**Aug 14, 2025**

**jasmine.park** 09:00 AM
Anyone have the swag count for Dreamforce? We need 500 hoodies and 1,000 socks.

**maya.chen** 09:15 AM
Ordered! They should arrive at the SF office by Sept 1.
Total cost: $18,500. Which budget code should I use?

**lina.cho** 09:20 AM
Use `MKT-EVENTS-2025`.

**alex.wright** 10:00 AM
While we're talking Dreamforce—are we setting up a custom landing page for the booth? We need to make sure the QR codes have `utm_medium=event` and `utm_source=dreamforce2025`.

**maya.chen** 10:05 AM
Already done. I’m also adding `utm_content=booth-scanning` vs `utm_content=theatre-session` so we can see which location drives better leads.

---

**Sep 22, 2025**

**jorge.martinez** 04:00 PM
The CRM migration is complete! All attribution should be flowing through to BigQuery correctly now.

**alex.wright** 04:15 PM
Awesome. I’m running a validation script now...
Uh oh. Jorge, `fact_marketing_touches` is showing 0 rows for the last 4 hours.

**jorge.martinez** 04:20 PM
Checking... Dammit. The Fivetran connector paused because of a schema mismatch on the `lead_email_hash` field. Fixing it now.

**lina.cho** 04:30 PM
Can we please go one week without a "schema mismatch"?

---

**Oct 5, 2025**

**marcus.webb** 10:00 AM
Jasmine, the SDRs are saying that "Content" leads are taking way too long to close. Outbound is 60% of our pipeline, but these whitepaper leads just sit in "Discovery" for months.

**jasmine.park** 10:15 AM
The content leads are higher volume, Marcus. They feed the nurture tracks.
@alex.wright, what's the average sales cycle for `content` vs `outbound`?

**alex.wright** 11:00 AM
Querying `fact_opportunities`...
- Outbound: 82 days
- Content: 135 days
- Partner: 68 days (fastest)

**marcus.webb** 11:05 AM
There you go. I want more Partner leads.

**jasmine.park** 11:10 AM
We all do, Marcus. But we can't buy partner leads at the same scale as LinkedIn or Search.

---

**Nov 12, 2025**

**omar.haddad** 01:00 PM
Kestrel Networks (cust_000708) just churned. Budget cuts.

**lina.cho** 01:15 PM
Verified. Just saw the cancellation notice in Stripe. They were a Business tier customer, $10,430 MRR.
@alex.wright make sure to mark them as `churned` in the next dbt run.

**alex.wright** 01:20 PM
Already handled. Churn date set to 2025-11-12.

---

**Dec 15, 2025**

**jasmine.park** 03:00 PM
Let's talk 2026 planning. We need to hit $55M ARR by the end of next year. That means roughly $1.5M in new net ARR every month.

**alex.wright** 03:15 PM
Looking at current conversion rates:
To hit that, we need to increase our Lead-to-Opp conversion from 12% to 15%, or increase spend by about 30% on the high-performing channels (Search and Referral).

**maya.chen** 03:20 PM
Search is getting expensive. CPCs for "workflow automation" are up 40% year-over-year.

**jasmine.park** 03:25 PM
Then we need to get better at SEO and Content. I want to see a plan for "Organic" to hit 25% of total pipeline by Q3 2026.

---

**Jan 10, 2026**

**lina.cho** 09:00 AM
@alex.wright I’m seeing some weird numbers in the NRR report for Q4. Did you include the churned customers in the cohort?

**alex.wright** 09:15 AM
I used an inner join on `fact_subscriptions` for the start and end of the period.

**lina.cho** 09:20 AM
NO! That’s what I warned about. An inner join drops the churned customers (since they don't have a record at the end of the period). That inflates the NRR.
You need to do a `LEFT JOIN` from the start-period cohort and `COALESCE(end_mrr_usd, 0)`.
NRR should be around 1.07. If you see 1.15, it's wrong.

**alex.wright** 09:30 AM
Fixed. You're right. NRR is 1.074. GRR is 0.94.

---

**Feb 19, 2026**

**grace.liu** 11:00 AM
Sad news—Beacon Studios (cust_000287) churned.

**marcus.webb** 11:05 AM
Wait, they were Business tier and had 65 seats. I thought they were doing great?

**grace.liu** 11:10 AM
They were! NPS was a 9, and their utilization was through the roof. It wasn't us—their parent company got acquired and they're being forced to migrate to the parent company’s legacy tool.

**lina.cho** 11:15 AM
That hurts. ~$116k ARR gone for reasons outside our control.

---

**Mar 5, 2026**

**jasmine.park** 08:00 AM
Board deck prep time again. @alex.wright I need "Bookings by First Touch Channel" for Q1 (to date).

**alex.wright** 09:45 AM
Here you go, Jasmine:

```sql
SELECT
  first_touch_channel,
  SUM(bookings_acv_usd) as total_bookings
FROM nexus-analyst-demo.acme.bookings_attribution
WHERE closed_won_at BETWEEN '2026-01-01' AND '2026-03-05'
GROUP BY 1
ORDER BY 2 DESC
```

| first_touch_channel | total_bookings |
|---------------------|----------------|
| outbound            | 1,450,000      |
| partner             | 820,000        |
| inbound             | 610,000        |
| paid_search         | 440,000        |
| referral            | 310,000        |
| event               | 150,000        |
| content             | 120,000        |
| organic             | 95,000         |

**jasmine.park** 10:00 AM
Outbound is still carrying us. I was hoping to see Inbound/Organic higher after the January push.

**maya.chen** 10:05 AM
The January push won't show up in "Bookings" for at least another 60-90 days given our sales cycle. But the `fact_marketing_touches` for `organic` are up 45% MoM. The pipeline is coming.

---

**Apr 12, 2026**

**jorge.martinez** 11:00 AM
Hey @channel — just a reminder that the `account_health` table in BigQuery is now the source of truth for "Engaged" status.
A customer is `is_engaged` if they have:
1. ≥3 active users
2. ≥10 successful workflow runs in trailing 28 days.

We recalibrated this in Q4 because the old definition (1 user, 1 run) was way too loose and giving us false positives on health.

**alex.wright** 11:15 AM
Does this affect the "at_risk" flag?

**jorge.martinez** 11:20 AM
Yes. `at_risk` now also includes if they have an open P1 ticket for >48h or a recent NPS detractor.
And for Enterprise customers, `critical` status is ONLY triggered by uncollectible invoices, since seat utilization rules don't apply to their unlimited plans.

---

**Apr 28, 2026**

**maya.chen** 02:00 PM
Has anyone looked at the ROAS for the APAC "Logistics Leaders" event?

**alex.wright** 02:15 PM
Yarrow Logistics (cust_000703) and Harbor Dynamics (cust_000713) both came from that.
Yarrow: $17,880 MRR ($214k ACV)
Harbor: $22,350 MRR ($268k ACV)
Total Bookings: $482,000
Event Cost: $50,000
ROAS: 9.6x — that was a massive win.

**jasmine.park** 02:20 PM
🔥 Let's do more of those. Can we find similar events in EMEA for Q3?

---

**May 1, 2026**

**alex.wright** 09:00 AM
@lina.cho I was trying to query `acme.marts.marketing.touches` and got a 404. Did we move it?

**lina.cho** 09:10 AM
Alex, we’ve talked about this. The BigQuery dataset is FLAT. There are no sub-datasets like `marts.marketing`.
The table is `nexus-analyst-demo.acme.fact_marketing_touches`.
The folder structure you see in dbt is just for our files, it doesn't translate to the SQL path.

**alex.wright** 09:12 AM
Right, right. My bad. Still drinking my first coffee.

---

**May 4, 2026 (Today)**

**jasmine.park** 08:30 AM
Morning team. Big day for board prep.
Alex, I need the final NRR and ARR numbers for the April close.
Lina, I need the "Critical Accounts" list for Marcus's slide.
Maya, give me the top 3 campaigns by "Pipeline Sourced" for the last 6 months.

**alex.wright** 08:45 AM
On it. Pulling from `nexus-analyst-demo.acme.arr_snapshot` and `nrr_trailing_12` now.

**maya.chen** 08:50 AM
Top 3 campaigns (by pipeline $):
1. LinkedIn - Enterprise Automation Series
2. Organic - "Scaling SaaS Workflows" Blog Post
3. Partner - Dutch Cloud Collective Q1 Referral Program

**jorge.martinez** 09:10 AM
Wait, before you send those—I'm seeing a double-count on Onyx Robotics (cust_000704). They upgraded to Enterprise but the old Business subscription hasn't been marked as `is_current = false` in the warehouse yet.

**lina.cho** 09:15 AM
@jorge.martinez fix it fast. I don't want to present inflated ARR to Rachel.

**jorge.martinez** 09:20 AM
Triggering a manual dbt run now. Should be clean in 10 mins.

---

**Thread: Swag Strategy for 2026**
*maya.chen (Mar 10, 2026):* Thinking about shifting from hoodies to high-quality tech pouches. Better brand longevity?
*jasmine.park:* I like it. Let’s get samples.
*alex.wright:* Can we make sure the pouches have a QR code on the inside?
*maya.chen:* lol Alex, you want a UTM on a tech pouch?
*alex.wright:* If someone scans it to get the "hidden" documentation link, why not?
*marcus.webb:* Please don't over-engineer the socks, guys.

**Thread: The "VRS" Column Mystery**
*alex.wright (Feb 5, 2026):* Hey @rajiv.menon, I see `vrs_band` in the data dictionary for `account_health` but the column is empty in BigQuery.
*rajiv.menon:* Ah, yeah. The "Value Realization Score" is a parked spec. We never actually built the logic for it. Just ignore it and use `account_health_status` for now.
*alex.wright:* Cool, thought I was going crazy.

**Thread: Webinar Glitch**
*maya.chen (Apr 15, 2026):* The Zoom-to-CRM integration just dumped 400 leads into the "General" bucket instead of the "Workflow Best Practices" campaign.
*jorge.martinez:* I see it. It looks like the API key expired mid-stream. I'm re-syncing them now.
*sarah.chen:* Are these actually good leads? Or just more bots?
*maya.chen:* 80% look like corporate emails. 20% are gmail/protonmail.

**Thread: Monthly Coffee Poll**
*alex.wright (Jan 5, 2026):* SF Office: Do we want to switch the beans in the kitchen?
- Blue Bottle (12 votes)
- Sightglass (8 votes)
- Peet's (1 vote - @jorge.martinez why?)
- "Just give me caffeine" (15 votes)

**Thread: Outbound vs Bookings Discrepancy**
*marcus.webb (Mar 20, 2026):* Alex, why does my report say outbound is $1.4M but the finance report says $1.2M?
*alex.wright:* Finance is likely looking at `fact_invoices` (cash collected), whereas we're looking at `bookings_attribution` (contract signed). Also, check if you're looking at ACV vs ARR.
*lina.cho:* Marcus, it's also the "Beacon Studios" effect. We booked them at the start of the year, but they churned before the first full payment hit.
*marcus.webb:* Got it. I hate churn.

**Thread: Email Deliverability**
*maya.chen (Feb 22, 2026):* Our open rates for the "Pro-to-Business" upgrade sequence dropped from 35% to 12% this week.
*jorge.martinez:* Checking the SPF/DKIM records...
*jorge.martinez:* Someone (no names mentioned) added a new marketing tool that didn't have the proper authorization. We were being flagged as spam by Outlook.
*jasmine.park:* @jorge.martinez fix it. That's our primary expansion funnel.

**Thread: EMEA Office Opening**
*jasmine.park (Nov 5, 2025):* The Amsterdam office opening event is next week. We have 200 confirmed RSVPs.
*maya.chen:* Do we have the "Acme Amsterdam" shirts ready?
*jasmine.park:* Yes, and they look great.
*alex.wright:* Did we set up a regional UTM for the RSVP page?
*maya.chen:* `utm_region=emea`. Don't worry, Alex. I've got you.

**Thread: Data Refresh Lag**
*alex.wright (Jan 12, 2026):* Is the warehouse lagging? I just saw a deal close in the CRM but it's not in BQ.
*david.kim:* Yeah, we have a 2-hour lag between the production DB and the warehouse. It should be there by 11:00 AM.
*alex.wright:* Thanks, David.

**Thread: Industry Breakdown**
*jasmine.park (Apr 1, 2026):* What’s our best performing industry by ACV?
*alex.wright:*
1. Fintech (Lead: Cobalt Systems, Sable Analytics)
2. Logistics (Lead: Yarrow Logistics, Ember Industries)
3. Healthtech (Lead: Marigold Health, Quartz Foundry)
Fintech has the highest average seat count (avg 75), but Logistics has the fastest sales cycle.

**Thread: UTM tagging for Partners**
*maya.chen (Dec 10, 2025):* I’m seeing `utm_source=partner_referral` and `utm_source=partner-referral`.
*alex.wright:* I’ll update the dbt model to `LOWER(REPLACE(utm_source, '-', '_'))`.
*jorge.martinez:* Or we could just tell the partners what to use?
*maya.chen:* Good luck with that.

**Thread: Salesforce vs Looker**
*sarah.chen (Mar 25, 2026):* Why is my quota attainment lower in Looker than it is in my spreadsheet?
*lina.cho:* Because your spreadsheet includes "Verbal Commits" and Looker only includes "Closed-Won" with a signed contract in the `fact_opportunities` table.
*sarah.chen:* Oh. Right. I'm still waiting on signatures for Onyx Robotics.
*marcus.webb:* Close it, Sarah! Quarter ends in 6 days.

**Thread: Dashboard Maintenance**
*alex.wright (May 4, 2026):* Updated the "Marketing Overview" dashboard. It now includes a toggle for `account_tier` (SMB, MM, Ent).
*jasmine.park:* Love the toggle. Can we also add a view for "Paused" customers?
*lina.cho:* Just a heads up, Tamarind Group (cust_000706) is the only "Paused" Business customer right now. Most just churn.
*jasmine.park:* Let's include it anyway, we might see more in Q2 with the current economy.

**Thread: Lead Scoring V2**
*maya.chen (Feb 15, 2026):* We’re rolling out the new lead scoring model. It gives extra points for "SOC2" and "Audit Logs" keyword searches.
*marcus.webb:* That sounds like Enterprise intent. I like it.
*alex.wright:* I'll track the conversion rate of "High Score" leads vs the old baseline.

**Thread: Slack Integration Test**
*maya.chen (Apr 30, 2026):* Testing the new automated "Deal Won" bot.
*bot:* :tada: NEW DEAL: Onyx Robotics (cust_000704) - Enterprise Tier - $420,000 ACV - AE: Tom Becker.
*marcus.webb:* THERE IT IS! Nice work Tom!
*jasmine.park:* Huge! What was the first touch?
*alex.wright:* `outbound` - Tom's been hunting them since 2025.

**Thread: Q1 Review Prep**
*jasmine.park (Apr 5, 2026):* Alex, for the Q1 review, I want to see a chart of "Spend vs Pipeline" by month.
*alex.wright:* On it. I'll join `fact_marketing_touches` with the spend export from the Finance team.
*lina.cho:* Use the spend numbers from the `mkt_spend_actuals` table, not the budget spreadsheet. The budget changed three times in March.

**Thread: NPS Responses**
*grace.liu (Jan 20, 2026):* Some great feedback from Sable Analytics (cust_000710) in the latest NPS run.
*alex.wright:* They gave us a 10. Comment: "Best automation tool we've used. The SOC2 compliance made the security review a breeze."
*jasmine.park:* That's a great quote for the next case study. Maya, can we reach out?
*maya.chen:* Already on it.

**Thread: Website Redesign**
*jasmine.park (Mar 15, 2026):* The new homepage is live!
*alex.wright:* Tracking looks good. `event_name = 'page_view'` is firing correctly on the new hero section.
*maya.chen:* I'm seeing a 5% increase in "Sign Up" clicks already.
*jorge.martinez:* Just make sure the `invited_by_user_id` is still being captured for the referral program.
*alex.wright:* Checked. It's in the `fact_user_events` properties_json.

**Thread: Late Night SQL**
*alex.wright (May 3, 2026 11:45 PM):* Why is `current_mrr_usd` in `dim_customers` different from `mrr_usd` in `fact_subscriptions`?
*lina.cho (May 4, 2026 08:30 AM):* Because `dim_customers` is an SCD (Slowly Changing Dimension) that refreshes once a day, while `fact_subscriptions` is updated every 2 hours from the raw events. Always use `fact_subscriptions` for the most recent MRR.

**Thread: Board Deck Final Polish**
*jasmine.park (May 4, 2026 10:00 AM):* Alex, the "Bookings by Channel" chart looks perfect. Ready to send to Rachel.
*alex.wright:* Great. I'll archive the query for next quarter.
*maya.chen:* Don't forget to update the date filters for the "Today" slide.
*jasmine.park:* Done. Let's do this. :rocket: