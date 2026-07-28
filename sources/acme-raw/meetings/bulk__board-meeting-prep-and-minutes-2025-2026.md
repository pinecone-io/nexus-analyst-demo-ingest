---
title: "Board meeting prep notes and minutes — Acme 2025-2026"
source_url: "internal://acme/board-meeting-prep-and-minutes-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Board of Directors: Working Document (2025-2026)

This workspace is for Sam (CEO), Rachel (CFO), and the executive team to prep for quarterly board meetings. **Keep all draft slides linked in the sub-pages.**

**Board Members:**
*   Sam Reyes (Acme, CEO)
*   Lisa Park (Lead Director)
*   Michael Torres (Ventures Cap)
*   Preet Kaur (Independent)

---

## Meeting Index
1. [Q1 2025 - February 12, 2025](#q1-2025)
2. [Q2 2025 - May 15, 2025](#q2-2025)
3. [Q3 2025 - August 20, 2025 (Series B Focus)](#q3-2025)
4. [Q4 2025 - November 18, 2025](#q4-2025)
5. [Q1 2026 - February 10, 2026](#q1-2026)
6. [Q2 2026 - May 04, 2026 (Upcoming)](#q2-2026)

---

<a name="q1-2025"></a>
## 🧊 Q1 2025 Board Prep (Feb 12, 2025)

### Prep Notes & Data Pulls
*   **Owner:** Rachel Stein
*   **Data Status:** Finalized as of Feb 10.
*   **Lina Cho:** I’ve updated the ARR figures. We are starting 2025 at **$33.2M ARR**. 
    *   *Note:* I used `nexus-analyst-demo.acme.arr_snapshot`. 
    *   **WARNING:** Do NOT use the Looker "Executive Summary" dashboard for the headline number. It’s still pulling from that old persistent derived table that caused the "$42M incident" last November. The board will lose it if we show them a $9M discrepancy again.
*   **Sam Reyes:** I need the NRR slide to be bulletproof. Michael is going to ask about the cohort.
*   **Rachel Stein:** @Lina, can you confirm the NRR calc for Michael? He asked last time if we drop churned customers from the denominator.
*   **Lina Cho:** No, we don't. The query `nexus-analyst-demo.acme.nrr_trailing_12` uses a fixed cohort from 12 months ago. We use a `LEFT JOIN` on the current MRR and `COALESCE(end_mrr_usd, 0)`. Churned customers stay in the denominator at $0. If we used an inner join, it would inflate NRR to like 120%, which is fake. Current NRR is **1.08**.

### Draft Talking Points
*   **Sam:** 2024 was about foundation. 2025 is about scaling the "Business" tier ($149/seat).
*   **Jasmine:** I’m presenting the "Bookings by Channel" slide. We’re seeing a lot of traction from "Partner" and "Outbound."
    *   *Question from Sam:* Are those ACV numbers monthly or annual?
    *   *Jasmine:* They are annual. `bookings_attribution.bookings_acv_usd` is already annualized in the warehouse. I checked with Rajiv. Do NOT multiply them by 12.

### Logistics
*   Catering: Blue Bottle coffee and assorted bagels (get the gluten-free ones for Preet).
*   AV: Michael’s laptop always has issues with the HDMI adapter. Have the USB-C dongle ready.

---

### Minutes: Q1 2025 Board Meeting
**Date:** Feb 12, 2025
**Attendees:** Sam, Rachel, Lisa, Michael, Preet.

**1. ARR & Growth**
*   Rachel presented $33.2M ARR. 
*   Michael: "Why is the Pro tier growth slowing?"
*   Sam: We are intentionally de-prioritizing Pro ($49/seat) to focus on the Business tier ($149/seat) where the retention is better. Pro is mostly self-serve and high noise for support.

**2. NRR Deep Dive**
*   Michael: "On the 1.08 NRR—is that trailing 12 on a fixed cohort?"
*   Lina (called into the room): "Yes, Michael. It’s a fixed cohort of customers who were active 12 months ago. Churned customers are kept in the calculation at zero value to ensure we aren't survivor-biasing the number."
*   Lisa: "What's the Gross Retention (GRR)?"
*   Rachel: "We don't have the GRR slide today, but it’s roughly 0.94. Most of the delta is expansion in the Enterprise accounts."

**3. Product Roadmap**
*   Dan Lee presented the vision for 2025.
*   Michael asked about "Value Realization." Dan mentioned a concept called VRS (Value Realization Score) they are drafting to track if customers are actually getting ROI, not just 'using' the tool.

**Action Items:**
*   [ ] Rachel to add GRR to the standard monthly reporting pack.
*   [ ] Dan to provide a more detailed spec on the VRS metric by next Q.

---

<a name="q2-2025"></a>
## 🌿 Q2 2025 Board Prep (May 15, 2025)

### Prep Notes
*   **Sam:** I want to highlight the Cobalt Systems (cust_000700) win. 80 seats on Business.
*   **Lina Cho:** Running the April close now. ARR is at **$34.8M**. 
    *   `SELECT sum(arr_usd) FROM nexus-analyst-demo.acme.arr_snapshot WHERE snapshot_date = '2025-04-30'`
*   **Jasmine:** Marketing spend is up. Cost per lead is stable, but we’re seeing a shift from Organic to Paid Search for the Business tier.
*   **Rachel:** Board is going to ask about the Series B timing. We need to look "fundable." That means clean data. 
    *   *Side note:* Someone keep an eye on the "Engaged Customer" metric. It looks weird in the draft deck.
    *   *Lina:* It’s because I filtered out the "Free" tier. We shouldn't report "Engaged" for people paying $0.

### Minutes: Q2 2025 Board Meeting
**Date:** May 15, 2025
**Attendees:** Sam, Rachel, Jasmine, Dan, Lisa, Michael, Preet.

**1. Marketing Attribution**
*   Jasmine presented the channel breakdown.
*   Preet: "The 'Referral' channel has the highest ACV. Are we incentivizing this?"
*   Jasmine: "Mostly organic word-of-mouth from engineers, but we are looking at a formal partner program."

**2. Series B Discussion**
*   Lisa: "If we want to go out in Q3, we need to show the path to $50M ARR."
*   Sam: "The pipeline for Enterprise is $12M right now. If we close 30%, we're on track."

**3. Product Update**
*   Dan: "We're starting to build the VRS (Value Realization Score) framework. It will track things like 'champion login recency' and 'integration depth'."
*   Michael: "Don't over-engineer it. Just tell me if they're using it."

---

<a name="q3-2025"></a>
## ☀️ Q3 2025 Board Prep (Aug 20, 2025)

### Prep Notes
*   **Series B Focus.** This is the big one.
*   **Lina Cho:** ARR is **$36.1M**.
*   **Sam:** We need the "Engaged" vs "Healthy" vs "At Risk" slide from Elena (CS).
*   **Elena Volkov:** I’m using `nexus-analyst-demo.acme.account_health`. 
    *   *Note for Sam:* 'At Risk' is defined as any account with an open P1 ticket > 48 hours OR a recent NPS detractor.
    *   *Lina:* Wait, check the Enterprise rules. For Enterprise (like Marigold Health, cust_000701), they don't go 'Critical' based on utilization because they have unlimited seats. They only go 'Critical' if they have an uncollectible invoice.
*   **Dan Lee:** I'm officially proposing the VRS project. We need $200k in headcount for the data engineering to build the real-time event pipeline.
*   **Rachel:** Let's see what the board says before we hire.

### Minutes: Q3 2025 Board Meeting
**Date:** Aug 20, 2025
**Special Guest:** Elena Volkov (VP CS)

**1. Fundraising**
*   Sam: "We have three term sheets. Lead is looking like $80M at a healthy valuation."
*   Lisa: "Congratulations. Now, don't spend it all at once."

**2. CS & Health**
*   Elena presented the health metrics.
*   Preet: "Why is Onyx Robotics (cust_000704) marked as 'Healthy Expansion' but they only have 500 seats on an Enterprise plan?"
*   Elena: "Their utilization band is > 0.6 and they have no open support issues. They are ripe for a seat expansion next year."

**3. VRS Proposal**
*   Dan Lee proposed the Value Realization Score.
*   Michael: "I'm skeptical. Why can't you just use the existing health score?"
*   Dan: "Health is reactive. VRS is proactive—it tells us if they are actually automating a core business process."
*   Board Consensus: Move forward with the spec, but don't hire yet. Use existing resources (Lina/Rajiv).

---

<a name="q4-2025"></a>
## 🍂 Q4 2025 Board Prep (Nov 18, 2025)

### Prep Notes
*   **Series B closed.** $80M in the bank.
*   **Lina Cho:** ARR is **$37.4M**.
*   **THE ENGAGEMENT DROP SCARE:**
    *   *Rachel:* "Lina, why did the 'Engaged Customer' count drop 15% in the draft slide? Sam is going to freak out."
    *   *Lina:* "It’s not a real drop in usage. Rajiv and I recalibrated the definition in `account_health.is_engaged`. We moved it from '1 active user' to '3 active users AND 10 successful runs'. The board wanted a tighter definition of value. I need to make sure this is clearly footnoted so they don't think the product is dying."
*   **Logistics:** The meeting is in the Amsterdam office (EMEA). Sam and Rachel are flying out. Lisa is joining via Zoom.

### Minutes: Q4 2025 Board Meeting
**Date:** Nov 18, 2025

**1. Post-Fundraising Operations**
*   Rachel: "Hiring plan is aggressive. We're looking for 15 new engineers in Q1."

**2. Engagement Recalibration**
*   Michael: "What happened to the engagement? These numbers look lower than Q3."
*   Sam: "We tightened the definition. We were being too generous. Now an 'Engaged Customer' actually means a team is using the product, not just one person logging in once a month. If you look at the old definition, we’d actually be up 4%."
*   Lisa: "Good. I prefer the honest metric."

**3. VRS Update**
*   Dan: "The VRS project is still in the 'spec' phase. We've realized the data collection is more complex than anticipated."
*   Sam: "We're parking VRS for now. We need the team focused on the Enterprise 'Audit Log' feature for the Q1 push."

---

<a name="q1-2026"></a>
## ❄️ Q1 2026 Board Prep (Feb 10, 2026)

### Prep Notes
*   **Owner:** Rachel Stein
*   **The Beacon Studios Churn:** This is going to be the main topic. 
*   **Lina Cho:** ARR at end of Jan was **$38.8M**. 
*   **Elena:** Churn analysis on Beacon Studios (cust_000287).
    *   Loss: ~$116K ARR.
    *   Reason: "Procurement/Parent Company." They were acquired by a conglomerate that uses a competitor. 
    *   *Signal Check:* Their account health was "Healthy" right up until the churn date (2026-02-18). NPS was 9. Utilization was high.
*   **Sam:** We need to explain why the "Health Model" didn't catch this.
*   **Rachel:** It’s because the health model tracks product usage, not M&A activity. 

### Minutes: Q1 2026 Board Meeting
**Date:** Feb 10, 2026

**1. Revenue Review**
*   Rachel: "ARR hit $38.8M. Good growth, but we had a big hit in Feb."

**2. Beacon Studios Churn Deep Dive**
*   Michael: "How did we lose a $116k account that was 'Healthy'?"
*   Elena: "It was a forced migration. Their new parent company has a global contract with a competitor. We were actually their preferred tool, but procurement overrode them."
*   Preet: "Are there other accounts in the 'Acquisition' danger zone?"
*   Elena: "We're auditing the top 50 Business accounts now."

**3. Pipeline**
*   Jasmine: "Bookings for Q1 look strong. Large Enterprise deal with Pebble Digital (expanding from Pro) and a new logo, Ember Industries (cust_000711)."

---

<a name="q2-2026"></a>
## 🌸 Q2 2026 Board Prep (May 04, 2026) - **DRAFT**

### Prep Notes
*   **Current Date:** 2026-05-04
*   **Headline ARR:** **$39.2M** (Final check: `nexus-analyst-demo.acme.arr_snapshot` for April 30).
*   **Lina Cho:** NRR is holding steady at **1.07**. 
    *   *Self-Correction:* I saw someone in Sales trying to calculate NRR by taking (Total ARR Today / Total ARR Year Ago). I told them that's wrong because it includes new logos. We are using the fixed cohort method for the board.
*   **Rachel:** We need to address the "VRS" question. Michael will remember we 'parked' it. 
*   **Dan Lee:** "VRS is officially parked due to competing priorities. We are using `account_health` as the proxy for now. The `vrs_band` column in the warehouse was never populated—don't let the board ask for it."
*   **Jasmine:** I'm presenting the Q1 Bookings by Channel. 
    *   Outbound: $420k
    *   Partner: $310k
    *   Organic: $115k
    *   *Reminder:* These are ACV. Do NOT let Sam say these are monthly.

### Draft Slides Checklist
- [ ] Headline ARR ($39.2M)
- [ ] NRR (1.07) and GRR (0.94)
- [ ] The "Beacon Studios" post-mortem summary
- [ ] Q1 Bookings by channel (Source: `bookings_attribution`)
- [ ] Enterprise Pipeline (Marigold Health expansion, Drag Industries renewal)

---

### Internal Email Thread (Pre-Meeting Noise)

**From:** Rachel Stein  
**To:** Sam Reyes, Lina Cho, Dan Lee  
**Date:** May 1, 2026  
**Subject:** Re: Board Deck - FINAL FINAL v3

Lina, 

Can you double check the seat count for Tamarind Group (cust_000706) in the 'At Risk' slide? The deck says 55 seats but I thought they paused?

**From:** Lina Cho  
**To:** Rachel Stein  
**Date:** May 1, 2026  

They are paused (as of Jan 2026). They still show up in `dim_customers` but their MRR is $0 in the fact tables. I’ll remove them from the 'At Risk' slide so we don't confuse Preet. 

Also, Sam—please don't mention the $42M figure again. That was a glitch in the old Looker PDT. The $39.2M is the source of truth from the `arr_snapshot` table. If Michael asks why growth looks 'slow', tell him it's because we're being more rigorous about churn timing.

**From:** Dan Lee  
**To:** Sam Reyes  
**Date:** May 2, 2026  

Sam, for the product slide, I'm just going to say VRS is 'in research' if it comes up. I don't want to say 'parked'—it sounds too negative. We're focusing on the Enterprise SSO and Audit Log features which are actually closing deals.

**From:** Sam Reyes  
**To:** Dan Lee  
**Date:** May 2, 2026  

Michael will see through 'in research.' Just say we prioritized the Enterprise roadmap to hit the $39M ARR target. He cares about the revenue more than the fancy metrics anyway.

---

### Meeting Logistics - May 4, 2026
*   **Location:** Boardroom 4A (The one with the working projector).
*   **Catering:** Order from the usual place. Michael wants the "Extra Spicy" tuna rolls. Preet is still GF. 
*   **Printouts:** 6 copies of the GAAP financials (Rachel has these). 
*   **Remote link:** Lisa Park is dialling in from London. Make sure the Owl camera is centered.

---

## Technical Appendix: Data Definitions for Board Reporting

**1. ARR (Annual Recurring Revenue)**
*   **Definition:** `SUM(mrr_usd) * 12`
*   **Source:** `nexus-analyst-demo.acme.arr_snapshot`
*   **Filters:** `is_current = TRUE`, `plan_tier != 'Free'`
*   **Note:** Do not use `dim_customers.current_mrr_usd` for historical board reporting as it does not snapshot.

**2. NRR (Net Revenue Retention)**
*   **Definition:** (MRR from 12mo cohort today) / (MRR from 12mo cohort 12 months ago).
*   **Source:** `nexus-analyst-demo.acme.nrr_trailing_12`
*   **Calculation Logic:** 
    ```sql
    -- Standard Board Logic
    SELECT 
        SUM(COALESCE(current_mrr, 0)) / SUM(baseline_mrr) as nrr
    FROM cohort_table
    -- Churned customers MUST stay in the denominator.
    ```

**3. Engaged Customer**
*   **Definition (Effective Q4 2025):** 
    *   `active_users_28d >= 3`
    *   `successful_workflow_runs_28d >= 10`
*   **Source:** `nexus-analyst-demo.acme.account_health`

**4. Bookings ACV**
*   **Definition:** The total annualized value of new contracts signed in the period.
*   **Source:** `nexus-analyst-demo.acme.bookings_attribution`
*   **Note:** This table only includes AE-led deals. PLG (self-serve) upgrades are excluded from this specific 'Bookings' view.

**5. Value Realization Score (VRS)**
*   **Status:** **PARKED**.
*   **Warning:** The columns `vrs_band` and `champion_login_recency` in `account_health` are currently NULL or contain legacy test data. Use `account_health_status` instead.

---
*End of Document*