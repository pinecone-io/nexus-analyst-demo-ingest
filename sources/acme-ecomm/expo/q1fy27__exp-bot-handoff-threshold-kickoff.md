---
title: "Expo experiment spec: 'Bot Handoff Threshold' kickoff (Care)"
source_url: "internal://acme-ecomm/expo/q1fy27__exp-bot-handoff-threshold-kickoff"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Kickoff Specification: Bot Handoff Threshold (`exp_2489`)

**Vertical:** Customer Care (`CARE`)  
**Sub-vertical:** Automate / Avoid  
**Owner:** aisha.rahman (Director PM Care, Automate/Avoid, `assoc_100130`)  
**Status:** `running` (Started: 2026-04-01)  
**Target Readout Date:** 2026-05-15  
**System of Record:** Expo (`dim_experiment` / `fact_experiment_readouts`, adapter: `expo_experiment`)  

---

## 1. Executive Summary & Context

Following the successful initial rollout and stabilization of the "Ask Acme v2" customer care deflection chatbot back on 2025-09-15 (under the leadership of dominic.paquet), the Automate & Avoid product team has been evaluating headroom for further deflection gains heading into Q1FY27 and Q2FY27. Deflection rate has climbed steadily from 39.5% in Q2FY26 to 45.0% in Q4FY26, and hit 49.6% following the close of Q1FY27. However, leadership has repeatedly emphasized that these aggregate gains must be scrutinized against customer satisfaction, particularly given the operational volatility experienced during the peak-season refund-delay crunch (when Medallia verbatims spiked and CSAT among deflected contacts dipped to 3.42). 

This experiment (`exp_2489`) tests a deliberate adjustment to the bot's conversation-state machine: delaying the point at which the bot offers or forces a handoff to a live human agent. By requiring the user to navigate one additional disambiguation or self-service confirmation node before triggering human escalation, we aim to measure whether additional intent-aligned deflection can be captured without degrading downstream customer sentiment beyond acceptable thresholds.

---

## 2. Hypothesis & Core Metrics

### Hypothesis
If we relax the strictness of the current conversational hand-off trigger in the Ask Acme v2 flow—specifically increasing the threshold of unresolved intent prompts from 2 to 3 iterations before presenting a live agent bridge—then total bot deflection rate will increase by at least 2.5 to 3.0 percentage points, while maintaining an acceptable guardrail CSAT floor among users who ultimately reach an escalated human agent.

### Primary Metric
- **Deflection Rate:** Percentage of total inbound care sessions resolved entirely within the bot tier without triggering a human handoff (`fact_care_contacts.deflected = true`). 
  - *Baseline (Q4FY26 / Q1FY27 exit):* ~49.6% to 52.1% blended run-rate.

### Guardrail Metric
- **CSAT Among Escalated Contacts:** Average CSAT score (1–5 scale, from `fact_care_contacts.csat_score`) restricted strictly to contacts that *did* escalate to a human agent (`deflected = false`). 
  - *Context & Sensitivity Warning:* CSAT-among-deflected has been a highly sensitive, tightly watched area throughout late FY26 and early FY27, heavily influenced by the Q4FY26 refund-delay dip (which saw deflected CSAT drop from 3.80 down to 3.42 before recovering to 3.55). The Care leadership team (hannah.brennan, dominic.paquet, and giulia.romano on the analytics side) is monitoring guardrails extremely closely. Any statistically significant degradation in escalated CSAT exceeding −0.20 points will trigger an immediate emergency review, regardless of top-line deflection gains.

---

## 3. Experimental Variants & Allocation

- **Control (`control` / `variant_a`):** Current production configuration of Ask Acme v2. Human hand-off triggers after 2 consecutive unresolved user intent loops or upon explicit user request ("talk to a human", "agent").
- **Treatment (`treatment_b`):** Relaxed hand-off threshold. Human hand-off triggers after 3 consecutive unresolved user intent loops, accompanied by an enhanced dynamic self-service suggestion card. Explicit user requests for a human continue to route immediately without friction to preserve baseline trust.

### Sample Size & Traffic Allocation
- **Traffic Split:** 50% Control / 50% Treatment across all incoming chat and bot-portal traffic in US, CA, and MX markets.
- **Target Sample Size:** Powered to detect a minimum detectable effect (MDE) of +1.0pp in deflection rate with $\alpha = 0.05$ and $\power = 0.80$, requiring approximately 450,000 exposed sessions over a 6-week observation window (April 1, 2026, through May 15, 2026).
- **Unit of Exposure:** Unique customer care session (`contact_id` in `fact_care_contacts`), tracked via `fact_experiment_exposures` capturing both `units_assigned` and `units_exposed` to guard against intent-to-treat (ITT) dilution.

---

## 4. Engineering & Data Notes

1. **Table Integration:** Daily exposure aggregates feed directly into `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`, and final metrics will populate into `fact_experiment_readouts` upon experiment conclusion on 2026-05-15.
2. **Confounding Checks:** Coordination with giulia.romano (Analytics Engineer, Care & VOC) ensures that the Medallia post-care survey stream (`fact_voc_responses` with `survey_type = 'post_care_contact'`) is tagged cleanly with experiment variant metadata to isolate guardrail CSAT from general seasonal satisfaction noise (such as residual sentiment from the Ontario returns processing normalization completed back in February).
3. **Partial Rollout Contingency:** As noted in preliminary planning notes with tara.oduya and aisha.rahman, if the experiment reads positively on May 15 without breaching the CSAT guardrail, a phased partial rollout (e.g., non-billing categories first) is scheduled for consideration starting May 20, 2026.

---
