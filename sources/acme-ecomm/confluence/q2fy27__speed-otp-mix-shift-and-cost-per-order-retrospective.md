---
title: "Confluence retrospective: Speed's blended OTP and cost-per-order, channel and mix detail"
source_url: "internal://acme-ecomm/confluence/q2fy27__speed-otp-mix-shift-and-cost-per-order-retrospective"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Speed & Fulfillment Retrospective: Blended OTP and Cost-Per-Order, Channel Detail (Q1FY26 – Q1FY27 Full Window)

**Owner:** `tara.oduya` (Director PM Speed & Fulfillment, `assoc_100140`)  
**Contributors:** `gabriel.stroud` (Fulfillment Ops Lead, `assoc_100330`), `amara.shah` (Data Analyst, `assoc_100211`)  
**Status:** Published / Archived for Leadership Review  
**Date:** July 20, 2026  

---

## 1. Executive Summary & Context

Now that the full six-quarter window from Q1FY26 through Q1FY27 is safely closed history (and as we sit deep inside Q2FY27 QTD pacing), this retro pulls the underlying channel- and cost-level data behind two headline Speed metrics that keep coming up together in Monthly Business Review (MBR) decks and executive alignment sessions:

1. **Blended On-Time-to-Promise (OTP):** Rose from **91.65% in Q1FY26** to **92.38% in Q1FY27** (+0.73pp).
2. **Cost Per Order:** Fell from **$7.85 to $7.30** across the exact same six quarters, featuring a steep drop concurrent with our DC sortation automation rollout.

In casual hallway discussions (and occasionally in Slack threads between product and finance), these two improvements sometimes get lumped together into a single narrative: *"Our DCs got automated, which made fulfillment faster and more reliable across the board."* 

This retro exists to put the channel-level OTP breakdown and the cost-per-order series side by side so that narrative can be checked against the underlying numbers, rather than assumed. Below: the OTP mart broken out by fulfillment channel and mix share, and the cost-per-order series alongside the DC automation and peak-season timeline. Read them together before drawing a conclusion about what drove which.

---

## 2. Decomposing On-Time-to-Promise: Rate vs. Mix

When we present the Speed vertical scorecard at the MBR, the blended on-time-to-promise figure is often treated as a monolithic indicator of fulfillment health. Let's look at what happens when we crack open the aggregate mart (`fulfillment_speed_daily`) and look at the underlying channels across the six completed quarters from Q1FY26 to Q1FY27:

| Fulfillment Channel | Q1FY26 | Q2FY26 | Q3FY26 | Q4FY26 | Q1FY27 |
|---|---|---|---|---|---|
| **Ship-to-Home OTP %** | 89.50% | 89.90% | 90.10% | 87.00% | 89.30% |
| **Pickup (BOPIS + Curbside) OTP %** | 99.50% | 99.40% | 99.50% | 99.10% | 99.60% |
| **DFS (Delivery From Store) OTP %** | 93.00% | 93.20% | 93.00% | 90.50% | 93.80% |
| **Blended OTP % (Headline)** | **91.65%** | **92.04%** | **92.31%** | **89.97%** | **92.38%** |
| Ship-to-Home Mix Share % | 77.5% | 76.5% | 75.4% | 74.0% | 68.9% |
| Pickup Mix Share % | 21.0% | 22.0% | 23.0% | 24.0% | 29.0% |

### Reading the Channel Rows

Observe the ship-to-home row. In Q1FY26, ship-to-home on-time performance stood at **89.50%**. In Q1FY27, ship-to-home OTP sat at **89.30%**—a net **decline of 0.20pp**. During Q4FY26 (the peak holiday quarter complicated by the JOL1 winter storm disruption on December 8, 2025), ship-to-home dipped to 87.00%.

The blended headline rose from **91.65% to 92.38% (+0.73pp)** over the same window. The mix share rows at the bottom of the table are part of that picture:
* **Pickup (BOPIS + curbside) mix share** rose from **21.0% in Q1FY26 to 29.0% in Q1FY27**—a **+8.0pp shift** in a single year.
* Pickup orders hit their promise window roughly **99.6% of the time** near-automatically, as they are fulfilled locally by store associates and triggered directly by the customer arriving on-site.

This mix shift coincided with the launch of the **"Pickup Perks"** campaign (`camp_90182` / `tara.oduya`) back on January 15, 2026, which incentivized local store pickup over shipping.

Readers doing the blended-vs-channel reconciliation themselves should note both facts sit in this same table: the channel-level trend and the mix-share trend, in the same window.

---

## 3. The Separate Cost-Per-Order Efficiency Story

While delivery reliability for ship-to-home remained flat-to-down slightly, our unit fulfillment economics followed a completely different trajectory. Across the same six completed quarters, the average cost per order (stamped in `fulfillment_speed_daily.avg_cost_per_order_usd`) fell steadily:

* **Q1FY26:** $7.85
* **Q2FY26:** $7.78
* **Q3FY26:** $7.70
* **Q4FY26:** $8.60 *(Peak / Holiday spike + JOL1 storm)*
* **Q1FY27:** $7.55
* *(For ongoing reference, Q2FY27 QTD is currently pacing at **$7.30**)*

### Dissecting the FON2 and JOL1 Automation Impact

The steepest single-quarter drop in the entire series—a massive **-$1.05 reduction**—occurred between **Q4FY26 and Q1FY27**. This drop coincided precisely with the deployment of **DC sortation automation Phase 1** at our Fontana (FON2) and Joliet (JOL1) distribution centers, which was phased in between January 12 and February 15, 2026 (led by `gabriel.stroud`).

As noted in past post-mortems, this exact same rollout window confounded Leo Brandt's "Wider Promise Window" experiment (`exp_1187`), making it impossible to cleanly isolate the experiment's delivery-promise effects from the simultaneous baseline improvements brought by the new mechanical sortation hardware.

One quarter-boundary fact worth flagging for anyone attributing the full -$1.05 drop to automation alone:
1. **The Holiday Reversion Effect:** Q4FY26 was the *only* quarter in the entire six-quarter history to exhibit a QoQ *increase* in cost per order (+$0.90, jumping from $7.70 to $8.60). This was driven by ordinary peak/holiday cost pressure, temporary surge labor premiums, and overtime at the Ontario returns center.
2. **Two Things Landing in the Same Quarter:** The automation rollout window (Jan 12–Feb 15) sits inside the same Q4→Q1 boundary as the shedding of that temp labor and premium freight surcharge. The two aren't separable at quarterly grain from this mart alone.

Reading the six-quarter series and the rollout timeline together is left to whoever is answering the sustainability question — the Q4 spike and the rollout dates are both in front of you above.

---

## 4. Reference: What's in This Mart

For future auditors and product teams referencing this document, both series sit in `fulfillment_speed_daily` at channel grain:

```
[Q1FY26 → Q1FY27 Window]
       │
       ├─► SPEED / OTP METRIC: Blended 91.65% → 92.38%; Ship-to-Home 89.50% → 89.30%; Pickup mix 21.0% → 29.0%
       │
       └─► COST PER ORDER: $7.85 → $7.30 QTD; DC automation rollout at FON2/JOL1 Jan 12–Feb 15; Q4 peak spike to $8.60
```

Whoever is briefing leadership on either metric should pull the channel-level and mix-share rows before citing the blended figure alone — they're what let you tell a real rate change apart from a shift in which channel is doing the work.

---

## 5. Confluence Discussion & Comments

> **`gabriel.stroud`** *(Fulfillment Ops Lead)* — 2026-07-21 09:14 AM  
> Looking back at the FON2/JOL1 rollout logs from February, our sort throughput per man-hour went up roughly 24% once the automated sorters bedded in. That's a mechanical throughput gain at the sort line — separate question whether it shows up the same way in over-the-road transit during a snowstorm. Worth Finance having the channel-level rows in front of them either way.

> **`amara.shah`** *(Data Analyst)* — 2026-07-21 10:32 AM  
> Thanks for putting this together, Tara. Will reference this exact page in the upcoming Q3 MBR prep deck. One minor note: make sure anyone querying the historical tables remembers that `fulfillment_speed_daily` is full-population aggregate grain, so the mix share calculations check out to 3 decimal places without needing to touch `fact_orders`.

> **`tara.oduya`** *(Director PM Speed)* — 2026-07-21 11:05 AM  
> @amara.shah - Agreed, added a explicit callout to `fulfillment_speed_daily` in the text. Let's make sure Leo sees this too before his next promise-window policy review.

---
### TODOs / Follow-Up Actions
* [ ] **`amara.shah`**: Update the internal Speed data dictionary snippet to explicitly link blended OTP changes to the BOPIS mix-share formula.
* [ ] **`tara.oduya`**: Brief Ben Tanaka (`assoc_100050`) on the ship-to-home OTP trend (-0.20pp) ahead of the August logistics sync.
* [ ] **`gabriel.stroud`**: Check if the JOL1/FON2 automation cost-per-order slope is leveling off in Q2FY27 QTD data or if there's additional headroom once Phase 2 rolls out later this year.

---
