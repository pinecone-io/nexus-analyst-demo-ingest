---
title: "Scratch — @marco.chen CSM call-prep notes April 2026"
source_url: "internal://acme/scratch/marco-csm-prep-2026-04"
license: "synthetic-demo"
attribution: "Internal scratch notes for CSM account management (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: scratch_note
---

# CSM Prep Notes — April 2026 (@marco.chen)

Just dumping thoughts here for the upcoming week. Need to cross-ref these with the `notion__csm-account-health-runbook.md` before the Monday sync with @elena.volkov.

## cust_000412 — Drag Industries (Q2 QBR)
*   **Context:** These guys were in the "critical" bucket for most of Feb (utilization < 0.20). We saved them with that custom 30-seat Business package @rachel.stein approved. 
*   **Health check:** `account_health_status` is finally back to 'stable' as of this morning's refresh. Successful runs are up 40% MoM.
*   **The Ask:** They are the perfect candidate for the **AI Workflow Assistant beta**. Their main builder (Avery) complained about step-configuration friction in the last Gong call. 
*   **Note:** Check if @dan.lee has the feature flag ready for them. If I can get them on the beta, it secures the renewal.
*   **Risk:** Still seeing some `AUTH_FAILED` spikes in `fact_workflow_runs`. Need to ask if they rotated their Salesforce tokens recently.

## cust_000087 — Halcyon Research (Renewal Close)
*   **Context:** Big 2-year multi-year deal on the table ($66K ARR expansion). See `gong__renewal__halcyon-research.md`.
*   **Red Flag:** Just saw an NPS detractor (score: 4) come in from their Engineering Lead (Sundara). Comment was something about "UI lag in the workflow builder." 
*   **Action:** Need to address this head-on before they sign the 2-year. If Sundara is unhappy, the whole deal is shaky. 
*   **Data Check:** Look at `fact_user_events` for Sundara specifically—is it just one bad session or a trend? @david.kim, can we pull latency logs for their org?
*   **Plan:** Acknowledge the NPS score, show them the H2 roadmap for builder performance. Don't let them stall the signature.

## cust_000223 — Veloce Logistics (Expansion Handoff)
*   **Context:** Utilization is sitting at 0.92. They are literally out of seats and have 5 people in the "invited" state who can't join. 
*   **Handoff:** Tagging @sarah.lopez for the seat expansion. They want to add 25 seats immediately. 
*   **Upsell:** They’re on Business but asking about "unlimited audit logs"—classic Enterprise signal. 
*   **Note:** Mention the SCIM provisioning requirement they brought up last month. That's the hook for the Enterprise upgrade. 
*   **To-do:** Check `fact_marketing_touches` to see if they’ve been hitting the "Enterprise Features" pricing page. @jasmine.park, any recent webinar attendance from their team?

## Random / Misc
*   Need to update the `notion__csm-account-health-runbook.md` with that note about M&A pauses. Just had a Pro customer go dark because they got bought by a PE firm. 
*   The `acme-cs-bot` is still double-posting the `#cs-at-risk` alerts for accounts with multiple admins. Need to bug @david.kim to fix the join logic in `marts/cs/at_risk_alerts.sql`.
*   @rajiv.patel — let's look at the VRS draft again (`notion__draft__value-realization-score-spec.md`). I want to make sure "Champion Login Recency" is weighted higher for MM accounts. If the admin hasn't logged in for 14 days, the account is dead to me, even if the runs are successful.
