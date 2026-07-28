---
title: "Launch-review sync notes: Ask Acme v2's first full quarter"
source_url: "internal://acme-ecomm/meetings/q4fy26__ask-acme-v2-first-quarter-launch-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: meeting_notes
---

# Meeting Notes: Ask Acme v2 First Full Quarter Launch Review & Care Operations Sync

**Date:** January 20, 2026  
**Time:** 10:00 AM – 11:30 AM EST  
**Location:** Conference Room B (HQ-3) / Google Meet Hybrid  
**Facilitator:** hannah.brennan (SVP Customer Care)  
**Notetaker:** giulia.romano (Analytics Engineer, Care & VOC)  

## Attendees
- hannah.brennan (SVP Customer Care)
- dominic.paquet (Care Ops Lead)
- aisha.rahman (Director PM Care - Automate/Avoid)
- julian.moss (Sr PM Care - Optimize/Platform)
- giulia.romano (Analytics Engineer, Care & VOC)
- amara.shah (Data Analyst, Finance/MBR)
- felix.arroyo (SVP Product & Growth) — *joined for the first 20 minutes*
- carlos.figueroa (VP Data & Analytics) — *joined late for metric validation segment*
- maya.lindqvist (Director PM US Conversion & Traffic) — *brief drop-in regarding post-checkout escalation pathways*

---

## 1. Opening & Administrative Noise
- **hannah.brennan:** Morning everyone. Let's make sure we move briskly through the deck today. We have the MBR prep coming up next week, and I want to ensure our numbers on the Ask Acme v2 bot are airtight before we put them in front of deborah.osei. 
- **felix.arroyo:** Quick heads-up before I jump to the product sync: Product Ops is still pushing hard on getting everything migrated from the old Aitable setup over to Jira following that decision last week. If any of your teams have lingering roadmap cards floating around in Aitable that touch care-deflection workflows, please get them tagged properly so Nadia Esposito's team doesn't flag them in the audit.
- **dominic.panquet:** Understood, Felix. We’re clean on our end. All automated ticket-routing epics are in Jira.
- **hannah.brennan:** Alright, Dominic, take it away on the bot performance review.

---

## 2. Presenting Ask Acme v2 Performance (dominic.paquet)
- **dominic.paquet:** Thanks, Hannah. Today we’re looking at where we stand for Q4FY26. As you all recall back from our launch review, Ask Acme v2 went live in production across web, app, and member portals back on September 15, 2025—right on the heels of that messy counterfeit-listing spike we had to deal with in Marketplace over the summer, which incidentally drove a minor initial surge in inquiries about third-party authentication before things stabilized.
- **dominic.paquet:** Looking at the deflection trajectory across quarters, the numbers are encouraging. In Q2FY26 (pre-launch), our blended deflection rate sat at **39.5%**. In Q3FY26—our first partial/full quarter under v2—that climbed to **42.8%**. Now, as we sit here QTD in Q4FY26 with just a couple of weeks left before the fiscal year closes on January 31, our run-rate is pacing toward roughly **45%** overall for the quarter. 
- **amara.shah:** Just to interrupt briefly, Dominic—are we locking that 45% figure for the MBR deck, or keeping it soft as a QTD estimate since Q4 doesn't technically close until the end of next week?
- **dominic.paquet:** Definitely keep it as QTD-trending, Amara. Do not cite it as a closed quarter-end number yet. We've got the final holiday tail-end traffic winding down, and there are always late adjustments. 
- **hannah.paquet** *(clarifying)*: Yes, let's treat it as a pace of roughly 45% for now. But let's look at the customer satisfaction side of this, because that's where things get nuanced.

---

## 3. The CSAT & Inferential Attribution Caveat
- **dominic.paquet:** Right. Alongside that rise in deflection, our CSAT score for *deflected* contacts (users who interacted with the bot and didn't escalate to an agent) has softened slightly across the quarters: moving from **3.90** in Q1FY26 down to **3.85** in Q2FY26, **3.80** in Q3FY26, and currently tracking around **3.70** QTD here in Q4. Meanwhile, agent-assisted CSAT has remained remarkably stable, hovering between 4.20 and 4.35 across all those periods.
- **giulia.romano:** And we have to layer the operational context on top of that CSAT softening. Remember, we had that massive returns-processing bottleneck out at the Ontario, CA returns center (`node_id` structure in `dim_fulfillment_node`) that started blowing up right around Cyber Monday week (December 1). Medallia verbatims tagged to refund delays crossed our 10% verbatim-share threshold the week of December 15th, and our quantitative 4-week rolling `avg_refund_cycle_days` crossed the 5.0-day SLA alert threshold the first week of January (hitting 5.03 days), before Hannah's team and Gabriel Stroud’s fulfillment group finally got the Ontario staffing situation sorted out. 
- **hannah.brennan:** Exactly. So we cannot claim the bot is solely responsible for either the rise in deflection or the slight dip in deflected CSAT. 
- **dominic.paquet:** That’s the critical inferential-attribution point that our cross-quarter read needs to grapple with. Deflection was *already* climbing pre-bot—we saw a +2.3pp organic bump the quarter before v2 even launched. The bot is helping, no doubt, but attributing every tick upward purely to the NLP model ignores the fact that our automated category-routing rules and self-service order tracking have also matured. Plus, customers hitting the bot during peak holiday crunch when their refund was delayed by five days were naturally less thrilled with automated answers, which dragged down the deflected CSAT average.

---

## 4. Operational Digressions & Routine Noise
- **aisha.rahman:** Are we seeing any covariance between the bot deflection rates and the recent pickup-perks push? Tara Oduya's team launched those BOPIS/curbside discounts on January 15th, and I wondered if more store-pickup orders mean fewer shipping-delay inquiries hitting care.
- **julian.moss:** I checked `fact_care_contacts` yesterday afternoon—volume on shipping inquiries is down slightly, but BOPIS location-finding questions are ticking up. It's a wash net-net. By the way, is anyone else having trouble with the Compass dashboard caching old marketplace numbers? I had to manually clear my session state because it was still pulling that stale $952.4M figure for Q4 Marketplace GMV instead of the restated $975.0M.
- **carlos.figueroa:** That Compass caching issue is a known artifact of the dbt model refresh cycle on the analytics cluster, Julian. Connor Blake pushed a patch to the Airflow DAG yesterday evening; it should be flushed out by tomorrow morning's ETL run. Make sure you aren't querying `acme_ecomm.marts.membership.member_cltv` with the old nested path syntax either—remember we flattened all dataset paths back in Q1. It's just `acme_ecomm.member_cltv` now.
- **amara.shah:** Noted, Carlos. Thanks.
- **hannah.brennan:** Alright, let's bring it back. Dominic, what are our next steps for the rest of Q4 and looking ahead to Q1FY27?

---

## 5. Action Items & Next Review Scheduling
1. **Dominic Paquet / Giulia Romano:** Finalize the Ask Acme v2 quarterly performance slide for the upcoming MBR deck, ensuring the 45% deflection metric is explicitly labeled as *QTD pace* and contextualized alongside the Ontario returns-delay CSAT impact.
2. **Aisha Rahman:** Prepare the preliminary experimental design for the upcoming "Handoff Threshold" test (`exp_2489`), scheduled to kick off in early Q1FY27.
3. **Giulia Romano:** Run a secondary correlation check between `fact_care_contacts` deflection flags and `fact_voc_responses` to isolate refund-delay verbatims from true bot interaction sentiment before the leadership readout.
4. **Next Review:** Schedule the pre-MBR deep-dive sync for next Tuesday, January 27, at 2:00 PM EST in Conference Room A.

---
*Meeting adjourned at 11:15 AM.*
