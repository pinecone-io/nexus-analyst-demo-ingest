---
title: "MBR notes: April 2025 Monthly Business Review, Q1FY26 QTD"
source_url: "internal://acme-ecomm/meetings/q1fy26__april-mbr-q1fy26-qtd-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-04-15T12:00:00+00:00'
adapter: mbr_deck_notes
---

# Acme eCommerce — Monthly Business Review (April 2025)
**Date:** Tuesday, April 15, 2025  
**Time:** 10:00 AM – 12:30 PM ET  
**Location:** HQ Conference Room 4A / Zoom Hybrid  
**Chair:** deborah.osei (CEO)  
**Lead Presenter:** carlos.figueroa (VP Data & Analytics — noting for the record this is his first MBR presenting in his new VP seat following his March 10 promotion)  
**Minutes Prepared By:** amara.shah (Data Analyst, Finance/MBR)

---

## 1. Administrative & Room Noise (10:00 - 10:15 AM)
- **Attendance Check:** Deborah Osei, Felix Arroyo, Hannah Brennan, Victor Okonkwo, Renee Kowalski, Ben Tanaka, Carlos Figueroa, Nadia Esposito, Maya Lindqvist, Owen Faust, Sanjay Bhatt, Ines Delgado, Noah Kessler, Aisha Rahman, Julian Moss, Tara Oduya, Leo Brandt, Simone Laurent, Derek Holloway, Malik Hendon, Wei Hartono, Amara Shah, Connor Blake, Giulia Romano, Dominic Paquet, Lucia Ferreira, Gabriel Stroud. (Absences: none noted; full executive and vertical PM roster present).
- **Logistical Note:** Coffee and pastries provided by the workplace team (courtesy of room 4A booking grace period). Reminder that the Looker-to-Compass-analog dashboard migration is rolling out for finance teams this week; Connor Blake noted that anyone seeing stale caching on Marketplace GMV should force-refresh their local Compass view (pointing out specifically that Compass PDT may still show the old Q4 figures if cached, though our canonical marts are clean).
- **Opening Remarks:** Deborah opened with a nod to the team's ongoing execution as we sit roughly two weeks out from the close of Q1FY26 (the quarter officially wraps on April 30, 2025). She specifically congratulated carlos.figueroa on stepping into the VP Data & Analytics role last month, noting how critical our telemetry hygiene has been as we scale past the $6.5B run-rate. Carlos took the floor to walk through the QTD pacing deck.

---

## 2. Executive Deck Presentation: Q1FY26 QTD Performance (10:15 - 11:15 AM)

Carlos Figueroa presented the aggregate scorecard. Because Q1FY26 is still in flight (16 days remaining until the April 30 hard close), all figures below are presented as **Quarter-to-Date (QTD) pacing**, not final quarterly closes. 

### A. US / CA / MX Conversion + Traffic (US_CONV — Deep Dive)
*Presenter: maya.lindqvist / owen.faust*
- **US Market Pacing:** Tracking to roughly **3.05%** US conversion rate and **$651.1M** US GMV for the full quarter pacing, driven by ~379.5M US sessions (down about 5.6% YoY, which felix.arroyo and the marketing team noted is an intentional pacing against paid-search efficiency targets rather than an organic traffic collapse). US orders are pacing to roughly 12.068M units at a $54.90 AOV.
- **CA & MX Markets:** Canada is pacing to ~42.12M sessions, 3.08% conversion, and $76.22M GMV. Mexico is pacing to ~26.94M sessions, 2.63% conversion, and $29.57M GMV. Carlos reminded the room of the stable structural gap where MX runs roughly 0.4–0.6pp below CA and 0.5–0.9pp below US across modeled quarters—this is a persistent baseline pattern, not a sudden trend deviation.
- **Item Page Surface / Iterations:** Maya Lindqvist highlighted that the Item Page Iteration program is moving right along. We’ve shipped early design adjustments on the US site, keeping our view-to-cart metrics stable. No major regressions to report from the web/app split.

### B. Marketplace (MARKETPLACE — Deep Dive)
*Presenter: victor.okonkwo / sanjay.bhatt / ines.delgado*
- **QTD Pacing by Sub-vertical:** 
  - **Style:** Pacing to **$543.0M** GMV for Q1FY26. (Victor noted that Style is seeing steady, healthy volume, though we are keeping an eye on category shifts as recommerce picks up speed).
  - **Resold:** Pacing to **$168.0M** GMV, continuing its explosive post-launch trajectory from prior quarters.
  - **Collectibles:** Pacing to **$104.0M** GMV. Following the viral card auction boom and the subsequent counterfeit-spike interventions last autumn, lucia.ferreira confirmed that the "Acme Verified" authentication workflow (partnered with GradeSure) is fully embedded. Collectibles return rates, which spiked up toward 11.2% during the Q3 chaos, have steadily normalized down toward ~5.4% as the verified badge program blankets active listings.
- **Seller Base:** The `dim_seller` panel reflects steady growth toward our ~2,560 active seller tracked threshold, with take rates holding strong around 13.5%.

### C. Customer Care (CARE — Deep Dive)
*Presenter: hannah.brennan / dominic.paquet*
- **Volume & Deflection:** Q1FY26 QTD contact volume is pacing to roughly **2,050K** contacts. Deflection percentage has climbed steadily to **49.6%**, aided by the ongoing maturation of the "Ask Acme v2" bot framework launched last fall.
- **CSAT & Handle Times:** Average handle time has dropped to an efficient **7.6 minutes** for agent-assisted contacts. CSAT for agent-assisted interactions holds high at **4.30**, while deflected user CSAT sits at **3.42** (down slightly from peak holiday compression, but well within normal operational bounds).
- **Historical Post-Mortem Note:** Hannah briefly reflected on the winter operational crunch (the December refund-delay spike tied to Ontario, CA returns center understaffing). She confirmed that staffing levels at Ontario were completely restored back in February 2026, and average refund cycle days have fully recovered to historical baselines (~3.3 days). The team agreed that the early warning threshold triggers worked as designed, even if executive escalation arrived slightly after Medallia verbatims first flagged it.

### D. Speed / Fulfillment (SPEED — Deep Dive)
*Presenter: tara.oduya / gabriel.stroud*
- **Mix Shifts:** Ship-to-home mix share is pacing at **68.9%** for Q1FY26 QTD, while Pickup (BOPIS + curbside) has expanded to **29.0%** (with DFS at **2.1%**). 
- **On-Time-to-Promise (OTP):** Blended on-time-to-promise is pacing to an excellent **92.38%** (Ship-to-home at 89.3%, Pickup at 99.6%, DFS at 93.8%). Tara reminded the room that the blended gain is largely a mix-share story: pickup orders pull the aggregate average up automatically due to their near-100% reliability, whereas ship-to-home requires heavier logistics management.
- **Cost Efficiency:** Cost per order is pacing down to **$7.55**, reflecting the durable efficiency gains harvested from the FON2 (Fontana) and JOL1 (Joliet) DC sortation automation phases implemented earlier this year.

### E. Membership — Acme+ (MEMBERSHIP — Deep Dive)
*Presenter: renee.kowalski / derek.holloway*
- **True Base & Net Adds:** Acme+ true active member base is pacing to reach **14.35M** by the end of Q1, with QTD net adds tracking at approximately **400K**.
- **Renewal & Benefits:** Annual renewal rate is pacing upward to **87.0%**. Derek Holloway noted that benefit adoption remains the single strongest lever for retention: members adopting 2+ benefits renew at 95%, compared to 71% for free-shipping-only members. The streaming bundle (via our current partner Vidora) continues to perform exceptionally well among users who are aware of it, though awareness campaigns remain a key priority for Q2.

---

## 3. Light Vertical Status Rows (Rapid Round-Robin)
Per meeting guidelines, the 11 light verticals were touched upon via a single status word to ensure cross-functional alignment without deep storylines:
- **CLUB:** Stable
- **B2B:** Expanding (malik.hendon noted strong early momentum with wholesale catalog onboarding)
- **PAYMENTS:** Nominal (dispute/settlement metrics tracking baseline)
- **OPD_DFS:** Growing (DFS volume healthily matching fulfillment speed projections)
- **MARTECH:** Optimized (reflecting the post-budget-adjustment marketing efficiency posture)
- **MPCX:** Steady
- **SPLITS:** Monitored
- **POR:** Recovered (post-Ontario normalization complete)
- **CSI:** Positive
- **REVIEWS:** Nominal
- **FS_LATER:** Stable

---

## 4. Open Discussion & Tangents (11:15 AM - 12:15 PM)
- **Conference Room AC & Office Logistics:** A brief 5-minute tangent occurred regarding the HVAC unit in the 4th-floor annex blowing directly onto the product operations team's desks. Nadia Esposito agreed to log a facilities ticket with office operations.
- **Aitable to Jira Migration Project:** Nadia provided a quick status update on the roadmap consolidation project kicked off back on January 15. Legacy Aitable cards are slowly being migrated over to Jira epics, though historical ideation records are taking longer than anticipated to scrub. Team leads were urged to ensure their Q2 planning tickets are fully populated in Jira by next Monday.
- **Team Lunch / Socials:** Renee Kowalski reminded everyone that the quarterly membership team lunch is scheduled for this Thursday at the cafeteria terrace, weather permitting.

---

## 5. Action Items & Next Steps
1. **carlos.figueroa / amara.shah:** Finalize the Q1FY26 MBR deck appendices following the April 30 quarter close and prep the final variance report for the May executive sync.
2. **nadia.esposito:** Follow up on the remaining Aitable-to-Jira ticket migrations for product operations before the end of the month.
3. **gabriel.stroud:** Provide a brief operational update on FON2/JOL1 DC automation maintenance windows at the next bi-weekly fulfillment sync.

**Next MBR Meeting Date:** Tuesday, May 20, 2025 (covering April 2025 close / Q2FY26 kick-off).

---
