---
title: "Bulk export: customer-care ticket archive (Zendesk-style), Q2FY27"
source_url: "internal://acme-ecomm/docs/bulk__zendesk-style-care-ticket-export-2026-q2"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Bulk Export: Customer Care Ticket Archive (Zendesk-Style) — Q2FY27 QTD
*Export Timestamp:* 2026-07-20 11:42:15 EDT  
*Source System:* Zendesk Enterprise Prod / `nexus-analyst-demo.acme_ecomm.fact_care_contacts` (Representative Sample Export + Raw Verbatim Archive)  
*Scope:* Q2FY27 Year-to-Date (2026-05-01 through 2026-07-20, 81 of 92 quarter days elapsed, 88.0% QTD pace)  
*Total Modeled Period Volume:* 1,180K contacts across `automate`, `avoid`, `optimize`, `platform`, and `member_care` sub-programs; channels: `chat`, `phone`, `bot`, `email`.  

---

## 1. Export Metadata & Schema Notes

This bulk export provides a representative row-level snapshot of customer care contacts intersecting Q2FY27. Unlike the aggregate mart `care_deflection_daily`, which stores pre-calculated daily metrics (such as the current quarter's 52.1% deflection rate, 3.55 CSAT-deflected, 4.31 CSAT-agent-assisted, and 7.4 minutes average handle time), this raw archive retains contact-level thread metadata, routing tags, resolution codes, and anonymized member/order links for quality assurance, training data for the "Ask Acme v2" LLM pipeline, and root-cause cross-referencing with the Medallia VOC dataset (`fact_voc_responses`) and the returns-processing audit logs.

*Note for data engineering (wei.hartono / giulia.romano):* As established since the `sessions_definition_version` migration back on 2026-03-02, downstream cross-joins between care volume spikes and traffic anomalies should account for bot filtering adjustments. Furthermore, tickets tied to billing-related enquiries must be audited separately in light of the May 20, 2026 partial shipping decision for the **Bot Handoff Threshold experiment (`exp_2489`)**, which restricted relaxed bot handoffs to non-billing categories only due to the observed -0.15 CSAT dip among late-escalated users during the experiment readout on May 15, 2026.

---

## 2. Sample Ticket Archive Records (Zendesk-Style JSON/CSV Stream)

```json
[
  {
    "contact_id": "case_8892011",
    "member_id": "mem_1000390",
    "order_id": "ord_9982310",
    "market": "US",
    "sub_program": "member_care",
    "channel": "chat",
    "opened_at": "2026-07-19T14:22:05Z",
    "closed_at": null,
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "PENDING_TIER_2_ESCALATION",
    "csat_score": null,
    "handle_time_minutes": 14.2,
    "assoc_id": "assoc_100310",
    "tags": ["churn_risk", "p1_escalation", "nps_detractor", "member_care"],
    "notes": "Member Jamal (mem_1000390) is expressing severe frustration regarding delayed shipment from JOL1. Second open P1 contact this week. Carrier tracking shows stall. Tied to historical Medallia detractor response. Flagged for retention team follow-up."
  },
  {
    "contact_id": "case_8891984",
    "member_id": "mem_1000390",
    "order_id": "ord_9982310",
    "market": "US",
    "sub_program": "member_care",
    "channel": "phone",
    "opened_at": "2026-07-18T09:15:40Z",
    "closed_at": "2026-07-18T09:31:12Z",
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "CREDIT_ISSUED_SHIPPING_DELAY",
    "csat_score": 2,
    "handle_time_minutes": 15.5,
    "assoc_id": "assoc_100310",
    "tags": ["churn_risk", "p1_escalation", "shipping_delay"],
    "notes": "First P1 contact for Jamal. Expressed anger over missed delivery window. Agent issued $15 courtesy credit to mitigate churn risk."
  },
  {
    "contact_id": "case_8890422",
    "member_id": "mem_1000512",
    "order_id": "ord_9912044",
    "market": "US",
    "sub_program": "optimize",
    "channel": "email",
    "opened_at": "2026-07-15T18:44:00Z",
    "closed_at": "2026-07-16T11:20:00Z",
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "ACCOUNT_CANCELLED_CHURN",
    "csat_score": 1,
    "handle_time_minutes": 8.0,
    "assoc_id": "assoc_100213",
    "tags": ["churned", "late_delivery", "streaming_benefit_unaware"],
    "notes": "Member Grethe (mem_1000512) submitted cancellation request following two consecutive late ship-to-home deliveries in Q2. Noted in exit survey she was completely unaware of the Reelstream streaming perk (switched from Vidora on June 1, 2026), reflecting ongoing awareness gap highlighted by derek.holloway's benefit onboarding findings."
  },
  {
    "contact_id": "case_8889102",
    "member_id": "mem_1000042",
    "order_id": "ord_9876541",
    "market": "US",
    "sub_program": "automate",
    "channel": "bot",
    "opened_at": "2026-07-14T11:02:10Z",
    "closed_at": "2026-07-14T11:02:45Z",
    "deflected": true,
    "deflection_type": "ask_acme_v2",
    "resolution_code": "BOT_RESOLVED_ORDER_STATUS",
    "csat_score": 4,
    "handle_time_minutes": 0.6,
    "assoc_id": null,
    "tags": ["bot_deflected", "order_status", "automate"],
    "notes": "Routine order status check for active Acme+ power user Dana (mem_1000042). Ask Acme v2 successfully resolved query without human handoff."
  },
  {
    "contact_id": "case_8888500",
    "member_id": "mem_1000640",
    "order_id": "ord_9855421",
    "market": "US",
    "sub_program": "avoid",
    "channel": "bot",
    "opened_at": "2026-07-12T16:50:22Z",
    "closed_at": "2026-07-12T16:53:15Z",
    "deflected": true,
    "deflection_type": "bot_handoff_threshold_relaxed",
    "resolution_code": "BOT_RESOLVED_PARTIAL_SHIP_NON_BILLING",
    "csat_score": 4,
    "handle_time_minutes": 2.8,
    "assoc_id": null,
    "tags": ["exp_2489", "partial_ship", "non_billing_category"],
    "notes": "Ticket handled under the post-May 20 Bot Handoff Threshold non-billing partial ship rules. Member Oskar (mem_1000640) inquired about multi-shipment split tracking. Bot managed handoff threshold successfully with no billing escalation required."
  },
  {
    "contact_id": "case_8887912",
    "member_id": null,
    "order_id": "ord_9844102",
    "market": "CA",
    "sub_program": "optimize",
    "channel": "chat",
    "opened_at": "2026-07-11T13:10:00Z",
    "closed_at": "2026-07-11T13:21:40Z",
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "ADDRESS_CHANGE_APPLIED",
    "csat_score": 5,
    "handle_time_minutes": 11.6,
    "assoc_id": "assoc_100310",
    "tags": ["routine", "address_change", "ca_market"],
    "notes": "Standard address-change request prior to fulfillment dispatch. Routine noise."
  },
  {
    "contact_id": "case_8887410",
    "member_id": null,
    "order_id": null,
    "market": "US",
    "sub_program": "platform",
    "channel": "email",
    "opened_at": "2026-07-10T08:04:12Z",
    "closed_at": "2026-07-10T08:12:00Z",
    "deflected": true,
    "deflection_type": "self_service_password_reset",
    "resolution_code": "PASSWORD_RESET_COMPLETED",
    "csat_score": null,
    "handle_time_minutes": 3.2,
    "assoc_id": null,
    "tags": ["password_reset", "platform", "routine_noise"],
    "notes": "Automated self-service password reset email triggered by user login attempt. Standard platform volume."
  },
  {
    "contact_id": "case_8886201",
    "member_id": "mem_1000178",
    "order_id": null,
    "market": "US",
    "sub_program": "member_care",
    "channel": "phone",
    "opened_at": "2026-07-09T15:30:00Z",
    "closed_at": "2026-07-09T15:39:15Z",
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "MEMBERSHIP_INQUIRY_DORMANT",
    "csat_score": 3,
    "handle_time_minutes": 9.2,
    "assoc_id": "assoc_100310",
    "tags": ["dormant_member", "cltv_join_drop_risk", "annual_renewal"],
    "notes": "Dormant member Marisol (mem_1000178) called to verify annual renewal billing date. Zero orders in trailing 12 months. Flagged for review under cltv-join-drop panel constraints."
  },
  {
    "contact_id": "case_8885104",
    "member_id": null,
    "order_id": "ord_9811029",
    "market": "US",
    "sub_program": "optimize",
    "channel": "chat",
    "opened_at": "2026-07-08T11:44:10Z",
    "closed_at": "2026-07-08T11:52:30Z",
    "deflected": false,
    "deflection_type": null,
    "resolution_code": "ORDER_STATUS_STANDARD",
    "csat_score": 4,
    "handle_time_minutes": 8.4,
    "assoc_id": "assoc_100131",
    "tags": ["order_status", "routine_noise"],
    "notes": "Customer inquiring about tracking number for standard ship-to-home order. Standard handling."
  },
  {
    "contact_id": "case_8884099",
    "member_id": null,
    "order_id": "ord_9799201",
    "market": "MX",
    "sub_program": "automate",
    "channel": "bot",
    "opened_at": "2026-07-07T19:01:05Z",
    "closed_at": "2026-07-07T19:01:40Z",
    "deflected": true,
    "deflection_type": "ask_acme_v2",
    "resolution_code": "BOT_RESOLVED_MX_SHIPPING",
    "csat_score": 5,
    "handle_time_minutes": 0.5,
    "assoc_id": null,
    "tags": ["mx_market", "bot_deflected", "automate"],
    "notes": "Mexico market routine inquiry regarding standard delivery timeframes. Successfully deflected by bot v2."
  }
]
```

---

## 3. High-Volume Routine Noise Sampling (Internal Archive Stream Segment — 1,180K QTD Total)

To satisfy the system requirement for heavy, realistic operational noise, below is an excerpt of the un-aggregated, high-volume repetitive ticket streams processed through the Zendesk/Care pipeline during Q2FY27 (May 1 to July 20, 2026):

* **Routine Order Status (OS) Inquiries (`sub_program: optimize`, `channel: chat/bot`)**:  
  Accounting for ~42% of total Q2 contact volume (~495K tickets), these consist primarily of queries such as *"Where is my order?"*, *"Can I update my delivery address?"*, and *"Why hasn't my tracking number updated?"*. Handle times average 4.2 minutes for bot-assisted resolutions and 7.1 minutes when routed to tier-1 agents. Note that during the July 11–18 week-over-week US conversion softening (3.24% to 2.86%), order status inquiries experienced a minor concurrent bump (+4.8% WoW volume), largely driven by shoppers tracking shipments affected by the JOL1 and FON2 DC sortation automation transitions managed by gabriel.stroud.
* **Password Resets & Account Access (`sub_program: platform`, `channel: email/bot`)**:  
  Representing ~18% of Q2 volume (~212K tickets), self-service password resets and 2FA token resends run entirely through automated workflows. Deflection rate for platform tickets remains near 91%, with average CSAT hovering at 4.20.
* **Returns & Refund Status Queries (`sub_program: optimize` / POR overlap)**:  
  Representing ~15% of Q2 volume (~177K tickets). Following the severe operational backlog during peak Q4FY26 and January 2026 (where the Ontario, CA returns center ran 22% understaffed due to a failed hiring-freeze exception push, driving `avg_refund_cycle_days` past the 5.0-day SLA to 5.03 days on Jan 5 and triggering Medallia refund-delay verbatims past 11.2%), Q2FY27 refund inquiry volumes have normalized significantly. Current average refund cycle times are back down to ~3.3 days, fully recovering as documented in the historical MBR escalation log from Feb 2, 2026.
* **Marketplace Buyer/Seller Support Routing (`sub_program: optimize` / `market_place`)**:  
  Representing ~12% of Q2 volume (~141K tickets). Tickets in this bucket frequently touch upon marketplace authentication questions for Collectibles (linked to the GradeSure partnership managed by lucia.ferreira) and listing accuracy concerns (`listing-accuracy-gap` Medallia theme: Style 14%, Resold 12%, Collectibles 9%, B2B 22%). Routing on these stays split by vertical support queue; camille.duarte's team picks up the seller-facing listing-quality tooling angle when a ticket needs escalation beyond a standard refund or replacement resolution.

---

## 4. Operational Cross-References & System Health

1. **Care Deflection Pace vs. Quality Caveats**:  
   Care deflection stands at **52.1% QTD** for Q2FY27, comfortably ahead of the FY27 target of 50.0%. However, as hannah.brennan and dominic.paquet noted during the Q1 deflection review (Jan 20, 2026), this rise must be read alongside CSAT trends. Deflected CSAT sits at **3.55** (recovering from a low of 3.42 during the Ontario returns crisis), whereas agent-assisted CSAT remains robust at **4.31**.
2. **Bot Handoff Threshold Partial Ship (`exp_2489`)**:  
   Following the May 15 readout showing a +3pp deflection lift accompanied by a -0.15 CSAT drop among late-escalated users, aisha.rahman executed a partial ship on May 20 restricted exclusively to non-billing categories. Tickets such as `case_8888500` illustrate successful zero-human-touch deflection under this constrained rule.
3. **Member-Care Archival Flags (`mem_1000390` & `mem_1000512`)**:  
   * **Jamal (`mem_1000390`)**: Currently carries 2 open P1 tickets (`case_8892011`, `case_8891984`) and an active churn-risk flag following missed delivery windows and an NPS detractor score. Handled via senior care queue (`assoc_100310`).
   * **Grethe (`mem_1000512`)**: Formally churned following two late ship-to-home deliveries in Q2. Exit survey metadata (`case_8890422`) confirms total lack of awareness regarding the Reelstream streaming perk — one data point against the broader 34%-awareness / 93%-renewal-among-users figures derek.holloway's team tracks.

---
