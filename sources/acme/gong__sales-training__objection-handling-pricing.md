---
title: "Gong sales training — pricing objection handling clinic"
source_url: "internal://acme/gong/sales-training/pricing-objections-2026-02-26"
license: "synthetic-demo"
attribution: "Acme Inc internal sales training (synthetic demo). Owner: Marcus Webb (VP Sales)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Pricing Objection Handling Clinic

**Date:** 2026-02-26  
**Host:** @marcus.webb (VP Sales)  
**Attendees:** Sales Team (MM/Ent AEs), Sales Ops (@jorge.martinez)  
**Recording Length:** 52:14  

---

**00:00** | **MARCUS WEBB** | Alright everyone, let's jump in. We’re seeing a trend in Q1 where "price" is cited as the primary loss reason in about 22% of our Closed_Lost opportunities (see `fact_opportunities.loss_reason`). Most of the time, that's not a budget problem—it's a value-articulation problem. Today we're doing a clinic on how to handle the "you're too expensive" or "the seat gap is too high" objections.

**02:15** | **MARCUS WEBB** | I’ve pulled four snippets from recent calls. I’ve anonymized the AEs, but I want us to listen to how we’re reacting when the customer flinches at the $149 Business tier.

**[SNIPPET 1 PLAYING]**  
**CUSTOMER:** "Wait, $149 a seat? Zapier is significantly cheaper for our team size. We only have 35 people who need this right now, so hitting a 50-seat minimum for Business is a non-starter."  
**AE:** "I totally understand. We can probably talk to my manager about a discount or maybe seeing if we can waive that seat minimum for the first year."  
**[SNIPPET 1 ENDS]**

**05:40** | **MARCUS WEBB** | Stop. What did we just see? The AE went straight to the discount lever before even defending the value. Per `notion__pricing-tiers.md`, we have a strict discount matrix. Jumping to a 10-20% discount or a seat-min waiver in the first five minutes of an objection kills your leverage. 

**07:12** | **MARCUS WEBB** | Instead of "I can talk to my manager," the pivot should be: "Zapier is great for simple task automation. Acme is for mission-critical infrastructure. If one of these workflows fails, what's the cost to your engineering team in manual recovery?" Pivot to ROI. Use the "Engaged Customer" logic from `glossary__engaged_customer.md`—explain that our most successful customers run 100k+ runs a month because they automate *entire departments*, not just tasks.

**12:45** | **SARAH LOPEZ** | Marcus, quick question on that. For the 30-40 seat customers, the jump from Pro ($49) to Business ($149) is a massive psychological cliff. It’s not just $100 more—it’s the 50-seat minimum. How do we bridge that $1,500/mo vs $7,500/mo gap without sounding like we're just taxing them for SSO?

**14:20** | **MARCUS WEBB** | Great point, Sarah. The "SSO Tax" is a real friction point. We know from `notion__pricing-tiers.md` that SSO is the gatekeeper for Business. But don't sell SSO. Sell the Audit Log and the SLA. If they are a 35-seat team in Finance or Healthcare, they *need* that 99.9% SLA and the 90-day audit trail for compliance. 

**16:30** | **MARCUS WEBB** | Also, remember the multi-year lever. If they commit to 2 years, we can do an 8% discount immediately without me even looking at it. That brings the effective rate down. If they need more, you escalate to me, but only if you have a clear path to a 250+ seat Enterprise expansion in 18 months.

**22:10** | **MARCUS WEBB** | Let's look at Snippet 2. This is a "Value Realization" play.

**[SNIPPET 2 PLAYING]**  
**CUSTOMER:** "We love the tool, but we're only using about 15% of our run quota on the Pro plan. Why would we move to Business?"  
**AE:** "The Business plan isn't just about the quota; it's about the complexity of the workflows you can build with our priority support team helping you architect them."  
**[SNIPPET 2 ENDS]**

**25:00** | **MARCUS WEBB** | This AE did it right. They moved away from "usage" (runs) and toward "outcomes" (architecture). Look at `dbt__model__account_health.md`. We know that "Stable" customers aren't just high-run customers; they are customers with high "unique workflows used." If a customer is only using 15% of their quota, they probably only have 2 workflows. Your job is to show them the 10 other templates in our library that solve their *other* problems.

**35:15** | **MARCUS WEBB** | Jorge, can you speak to the data on the "Price" loss reason?

**36:00** | **JORGE MARTINEZ** | Yeah. When we look at `marts/sales/bookings_attribution.sql`, the deals we win on "Price" objections usually have a higher `days_first_touch_to_won`. It takes longer to sell the value. If you're trying to close a Business deal in 30 days, you're going to get beat up on price. The average cycle for a successful Business win is closer to 65 days. Give yourself the time to do a proper discovery.

**42:10** | **MARCUS WEBB** | Last thing: the "Pro" price increase is coming June 15th ($49 -> $59). Use this as a forcing function for your current Pro-tier leads. "Hey, we're adjusting our Pro pricing soon, but if we get you onto a Business annual commit now, I can grandfather your seat rate and waive the first 5 seats of the minimum." That’s a @rachel.stein approved play for MM AEs.

**48:00** | **MARCUS WEBB** | Summary: 
1. Stop apologizing for the $149 price point. 
2. Reference the SLA and Audit Logs as "Enterprise-grade reliability," not "features."
3. Use multi-year discounts (5%/8%) to soften the blow.
4. If they are under the 50-seat min, sell the *future* state. "You're hiring 20 people this year; you'll hit this minimum by Q3 anyway."

**51:45** | **MARCUS WEBB** | Check the updated `notion__pricing-tiers.md` for the new discount approval workflows. Jorge just updated the Salesforce validation rules to match. Good selling.

---

**Action Items:**
- @jorge.martinez to update Salesforce "Loss Reason" picklist to include "Feature Gap: SSO" vs "Price: Seat Minimum".
- All AEs to review `gong__discovery__cust000412-drag-industries.md` for a masterclass in defending the Business tier to a 30-seat account.
- @marcus.webb to share the "ROI of Automation" slide deck in #sales-enablement.
