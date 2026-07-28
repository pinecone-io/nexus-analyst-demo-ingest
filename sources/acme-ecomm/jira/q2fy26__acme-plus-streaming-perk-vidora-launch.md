---
title: "Jira ticket: Acme+ streaming-perk launch, partner Vidora"
source_url: "internal://acme-ecomm/jira/q2fy26__acme-plus-streaming-perk-vidora-launch"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: jira_ticket
---

# MEM-4019: Acme+ streaming benefit launch (Partner: Vidora)

**Project:** Membership Growth & Retention (Acme+)  
**Epic:** MEM-3800 (FY26 Benefit Expansion Suite)  
**Key:** MEM-4019  
**Type:** Release / Epic Child  
**Status:** Done (Resolved 2025-06-01)  
**Priority:** P1 - High  
**Assignee:** renee.kowalski (SVP Membership, assoc_100040)  
**Reporter:** renee.kowalski  
**Contributors:** simone.laurent (assoc_100150), derek.holloway (assoc_100151)  
**Labels:** `acme-plus`, `streaming-benefit`, `vidora`, `release-q2`, `cltv-driver`  

---

### Description

This ticket tracks the production rollout of the new Acme+ streaming benefit, secured under our partnership agreement with **Vidora**, going live across all eligible active subscriber accounts starting **2025-06-01**. 

As discussed in last month's MBR syncs and following the FY26 kickoff leadership alignment led by felix.arroyo, our primary strategic lever for stabilizing and lifting annual renewal rates—currently pacing near 86%—is expanding non-shipping utility inside the core membership fee structure. Members frequently cite shipping speed (our baseline free expedited benefit) as table stakes, but long-term cohort retention requires emotional stickiness and digital day-to-day engagement. 

#### Benefit Mechanics
- **Inclusion:** Bundled directly into both monthly and annual Acme+ membership plans at **no extra cost** to the subscriber. There is no tiered add-on fee or hidden credit card upsell step.
- **Entitlement Flow:** Members authenticate via single sign-on (SSO) bridging our membership database (`dim_member`) to Vidora’s content delivery tier using their primary Acme account credentials.
- **Scope:** Full catalog access to Vidora's ad-supported and select premium on-demand streaming content, accessible via web, mobile app integration, and supported connected TV endpoints.

---

### Rollout Scope & Phasing

- **Phase 1 (Internal Dogfooding / Associate Test Group):** 2025-05-15 to 2025-05-22. Tested against internal associates (`assoc_` accounts) to verify token passing and SSO stability. Minor edge cases caught with Safari cookie partitioning; resolved by wei.hartono's data engineering team updating our session-cookie flags.
- **Phase 2 (Canary Release):** 2025-05-25 to 2025-05-31. 5% random rollout of active annual subscribers. Monitored error rates on API calls back to the BigQuery membership tables (`fact_membership_events`). Zero major regressions noted.
- **Phase 3 (General Availability):** **2025-06-01**. Full-scale exposure to 100% of active Acme+ members across US, CA, and MX markets.

---

### Forward-Looking Hypothesis & CLTV Modeling

*Note for downstream data teams (amara.shah, carlos.figueroa): Do not cite any mature-cohort renewal lift figures as immediate measured results for this launch. Because this release went live on 2025-06-01, we are operating on a forward-looking HYPOTHESIS rather than closed-cohort longitudinal reads:*

- **Hypothesis:** By bundling Vidora's streaming tier into the standard membership fee, we project that members who successfully adopt and engage with the streaming benefit within their first 30 days will exhibit an annual renewal rate lift comparable to our multi-benefit benchmark (moving from a baseline single-benefit/free-shipping-only renewal rate of ~71% toward a targeted 90%+ tier for multi-benefit adopters).
- **Caveat & Monitoring:** Awareness is our primary bottleneck. Drawing from our experience across other digital perks, initial discovery rarely exceeds 35% without explicit surfacing. Simone Laurent and Derek Holloway are already scoping a follow-up "Benefit Onboarding Carousel" experiment for later quarters to actively drive discovery and reduce the silent churn risk seen in dormant profiles (similar to the patterns identified in our `member_cltv` panel joins where unengaged members quietly slip away).

---

### Comments & Activity Stream

**2025-05-10 | renee.kowalski**  
Syncing with legal and Vidora account reps this morning regarding the final SLA additions for peak concurrent streams. Everything looks green for the May 15 dogfooding window. Simone, please ensure the customer care team (hannah.brennan, dominic.paquet) has the FAQ scripts ready in the "Ask Acme" knowledge base so agents aren't caught flat-footed when members ask how to activate their login.

**2025-05-18 | simone.laurent**  
@renee.kowalski Care scripts are uploaded to Confluence and pushed to Dominic's team. We ran a quick test with 50 internal folks yesterday; token exchange is clean. One minor note: make sure we aren't joining `dim_member` to `fact_orders` using an INNER JOIN when pulling our initial target audience lists for the email blast—let's remember the lessons from the `cltv-join-drop` bug so we don't accidentally drop zero-order active members who might still want to watch movies!

**2025-05-25 | derek.holloway**  
Canary traffic is looking stable. Vidora API latency is hovering around ~180ms, well within our 300ms threshold. No anomalous drops in site conversion across US_CONV. Proceeding with 100% GA cutover for June 1.

**2025-06-01 | renee.kowalski**  
**RELEASED.** Vidora streaming perk is officially live across all active Acme+ tiers as of 04:00 ET today. Monitoring dashboards in Compass are green. Closing out ticket as complete. Great work team—let's watch the benefit redemption counters closely in `fact_membership_events` over the next two weeks.

---
