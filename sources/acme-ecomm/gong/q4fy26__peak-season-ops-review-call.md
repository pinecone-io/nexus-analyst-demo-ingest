---
title: "Gong call transcript: peak-season (Black Friday/Cyber Monday) ops review call"
source_url: "internal://acme-ecomm/gong/q4fy26__peak-season-ops-review-call"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: gong_call
---

**Meeting Title:** Peak Season (Black Friday / Cyber Monday) Executive Operations Review  
**Date:** December 15, 2025  
**Participants:** 
- Ben Tanaka (`ben.tanaka`, SVP Supply Chain & Fulfillment)
- Gabriel Stroud (`gabriel.stroud`, Fulfillment Ops Lead, DC network)
- Tara Oduya (`tara.oduya`, Director PM Speed & Fulfillment)
- [System Note: Automated Gong Notetaker active, v4.12 - Transcription confidence 94.2%]

---

**[00:00:12] ben.tanaka:** Morning everyone. Let’s get straight into it. We've got the post-Cyber Monday week numbers locked across the board, and I want to walk through how the DC network actually absorbed the surge versus what we modeled back in October. Gabriel, let’s start with Joliet and Fontana throughput, and then Tara, we can touch on how the promise windows held up under the volume spike before we get into the holiday backlog.

**[00:00:44] gabriel.stroud:** Morning, Ben. Morning, Tara. Yeah, so looking at the numbers from the Black Friday surge through Cyber Monday week—remember, `camp_90214` and the main `camp_90214` traffic waves hit us right on schedule on November 28th—we actually handled total throughput pretty cleanly across the tier-1 nodes, with one major asterisk that everyone's tracking right now.

**[00:01:15] tara.oduya:** You mean JOL1.

**[00:01:18] gabriel.stroud:** Exactly. JOL1. We had the volume surge coming in right as that winter storm hit on December 8th. Thirty-six hours of total disruption at Joliet. It completely choked out our outbound trailer staging. Trucks couldn't get off the yard, and we were sitting on outbound dwell times pushing four times our normal average. 

**[00:01:52] ben.tanaka:** Right, and that's sitting directly on top of the staffing constraints we've been arguing about with HR for three months. Did the temporary contingency shifts help at all, or were we just spinning wheels?

**[00:02:10] gabriel.stroud:** They helped mitigate a total stop, but honestly, Ben, we were running on fumes. The temporary agency staffing pool in the greater Chicago market was completely tapped out because every other major box retailer was offering a five-dollar premium on the hourly rate. We matched it late, but by then we’d already lost two critical day shifts. 

**[00:02:44] tara.oduya:** From the promise side, customers felt that JOL1 bottleneck immediately. Even though our pickup channels—BOPIS and curbside—held up at over 99% on-time performance because store-level inventory buffers were thick enough, our ship-to-home promise accuracy out of the Midwest nodes took a noticeable hit during that second week of December. We're seeing it show up in the early Medallia verbatims coming across Hannah’s desk, too. People are starting to complain about tracking updates freezing right when packages hit the Joliet sort facility.

**[00:03:30] ben.tanaka:** Yeah, Giulia’s team flagged that the refund-delay and shipping-inquiry verbatims are creeping up in Medallia. Not at an alarm bell level yet, but it's ticking past our standard noise floor. We need to keep a very close eye on that over the next ten days so it doesn’t spill over into January chargebacks and customer service churn.

**[00:04:02] gabriel.stroud:** Agreed. On the bright side, Fontana—FON2—handled its volume profile almost without a hiccup. The new tilt-tray sorter calibration we ran back in October paid off. If FON2 hadn’t absorbed that overflow rerouted from JOL1 during the storm, Joliet would have completely flatlined.

**[00:04:31] ben.tanaka:** That’s a good transition. Looking ahead to next quarter—and I know we’re still right in the middle of peak execution, but finance is already leaning on us for the Q1 capital expenditure roadmap—we need to seriously look at what automation options we have on the table for FON2 and JOL1. I don't want to get caught with our pants down on temporary headcount shortages again next holiday, and frankly, the manual sortation bottlenecks are costing us too much in labor variance.

**[00:05:12] gabriel.stroud:** Yeah, absolutely, Ben. We’ve been quietly scoping some options with the industrial engineering vendors. Nothing formal yet, but we're looking at whether we can bring in automated induct systems and high-speed multi-chippers for the primary sort lines at both nodes. If we can get ahead of that, we might be able to pitch a phased rollout starting early next year. 

**[00:05:48] tara.oduya:** Just keep in mind if you're touching sortation lines in Q1, we have to coordinate around the wider promise window experiments Leo’s team is planning to roll out in January. If we’re modifying DC throughput mechanics at the same time we’re loosening promise displays on the frontend, we’re going to completely confound our delivery-speed attribution data. We won't know if an on-time bump came from the hardware upgrade or just lower consumer expectations on the checkout screen.

**[00:06:25] ben.tanaka:** Good catch, Tara. Let's make sure Leo is looped into the engineering sync next Tuesday so we don't trip over each other's experiment footprints. 

**[00:06:40] gabriel.stroud:** Will do. I’ll set up a quick 30-minute sync with Leo and his analytics counterpart before the end of the week. 

**[00:06:55] ben.tanaka:** Perfect. All right, let’s get back to the daily floor reports. Tara, send over that updated regional promise-hit breakdown once your morning batch finishes running in Compass. I want to see if the Northeast lanes recovered after the storm cleared out or if we're still seeing residual transit delays out of the eastern sort centers.

**[00:07:22] tara.oduya:** Will do, Ben. It'll be in your inbox by noon. 

**[00:07:28] ben.tanaka:** Thanks, team. Good hustle through the peak surge so far. Let's keep the communication tight through the end of the month. 

---
