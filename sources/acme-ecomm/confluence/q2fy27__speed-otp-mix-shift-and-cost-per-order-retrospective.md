---
title: "Confluence retrospective: Speed's blended on-time-to-promise mix-shift, and the separate cost-per-order efficiency story"
source_url: "internal://acme-ecomm/confluence/q2fy27__speed-otp-mix-shift-and-cost-per-order-retrospective"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Speed & Fulfillment Retrospective: Blended OTP Mix-Shift vs. Cost-Per-Order Efficiency (Q1FY26 – Q1FY27 Full Window)

**Owner:** `tara.oduya` (Director PM Speed & Fulfillment, `assoc_100140`)  
**Contributors:** `gabriel.stroud` (Fulfillment Ops Lead, `assoc_100330`), `amara.shah` (Data Analyst, `assoc_100211`)  
**Status:** Published / Archived for Leadership Review  
**Date:** July 20, 2026  

---

## 1. Executive Summary & Context

Now that the full six-quarter window from Q1FY26 through Q1FY27 is safely closed history (and as we sit deep inside Q2FY27 QTD pacing), it is time to put to bed a persistent analytical confusion that keeps resurfacing in our Monthly Business Review (MBR) decks and executive alignment sessions. 

For the past several quarters, executive leadership has looked at two headline metrics coming out of the Speed vertical and drawn intuitive—but incorrect—causal links between them:
1. **Blended On-Time-to-Promise (OTP):** Rose from **91.65% in Q1FY26** to **92.38% in Q1FY27** (+0.73pp).
2. **Cost Per Order:** Fell from **$7.85 to $7.30** across the exact same six quarters, featuring a steep drop concurrent with our DC sortation automation rollout.

In casual hallway discussions (and occasionally in Slack threads between product and finance), these two improvements have been lumped together into a tidy, satisfying narrative: *"Our DCs got automated, which made fulfillment faster and more reliable across the board."*

**That narrative is fundamentally false.** 

As we will demonstrate explicitly in this retro, these are two entirely different, real effects driven by distinct operational mechanics during the same window:
* **The OTP gain is a mix-shift phenomenon, not a rate improvement.** On-time-to-promise for our hardest, highest-volume channel (ship-to-home) actually *declined* slightly over the window (**89.50% -> 89.30%**, -0.20pp). The blended headline improved only because customer behavior shifted heavily toward store pickup (BOPIS/curbside), which runs at near-100% promise reliability by nature of being customer-triggered and same/next-day.
* **The cost-per-order drop is a genuine, durable efficiency gain.** Driven primarily by the DC sortation automation rollout at FON2 and JOL1 earlier this year (the same initiative that famously confounded Leo's "Wider Promise Window" experiment back in February), unit fulfillment costs fell significantly, even when accounting for post-holiday seasonal reversion.

Do not conflate the two. The DCs got more efficient (cost), but delivery did not get more reliable for our primary shipping channel (OTP rate). Let us walk through the data.

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

### The Finding: A Masterclass in Compositional Arithmetic

Observe the ship-to-home row. In Q1FY26, ship-to-home on-time performance stood at **89.50%**. In Q1FY27, after four quarters of optimization work, multiple experiment cycles, and major capital investments in our warehouse network, ship-to-home OTP sat at **89.30%**—a net **decline of 0.20pp**. 

For our most complex, highest-GMV channel—the one involving line-haul transit, carrier handoffs, and residential delivery exceptions—we did not move the needle forward on reliability. In fact, during Q4FY26 (the peak holiday quarter complicated by the JOL1 winter storm disruption on December 8, 2025), ship-to-home plummeted to 87.00%.

So how did the blended headline rise from **91.65% to 92.38% (+0.73pp)**?

Look at the mix share rows at the bottom of the table:
* **Pickup (BOPIS + curbside) mix share** rose from **21.0% in Q1FY26 to 29.0% in Q1FY27**—an astonishing **+8.0pp shift** in a single year.
* Pickup orders hit their promise window roughly **99.6% of the time** near-automatically, as they are fulfilled locally by store associates and triggered directly by the customer arriving on-site.

This structural shift was dramatically accelerated by the launch of the **"Pickup Perks"** campaign (`camp_90182` / `tara.oduya`) back on January 15, 2026, which incentivized local store pickup over shipping. Because a larger proportion of our total order volume was routed through a channel that is virtually immune to transit delays, the company-wide blended average was pulled upward.

**Bottom line for the record:** On-time-to-promise did not improve for our hardest channel. The blended number improved entirely because our order mix changed. 

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

However, we must apply an analytical caveat here to maintain intellectual honesty:
1. **The Holiday Reversion Effect:** Q4FY26 was the *only* quarter in the entire six-quarter history to exhibit a QoQ *increase* in cost per order (+$0.90, jumping from $7.70 to $8.60). This was driven by ordinary peak/holiday cost pressure, temporary surge labor premiums, and overtime at the Ontario returns center. 
2. **Post-Holiday Rebound vs. True Automation:** Part of the dramatic -$1.05 drop landing in Q1FY27 is therefore normal seasonal post-holiday reversion (shedding temp labor and premium freight surcharges), rather than automation acting in isolation.

**The Verdict:** Net of seasonal noise, the broader six-quarter decline from $7.85 down to $7.30 (current QTD pace) represents a genuine, durable structural efficiency gain. The sortation hardware at FON2 and JOL1 reduced manual touchpoints per unit, lowering labor overhead per package handled. 

---

## 4. Synthesis: Two Real Effects, One Window

To summarize for future auditors and product teams referencing this document:

```
[Q1FY26 → Q1FY27 Window]
       │
       ├─► SPEED / OTP METRIC: Blended +0.73pp (91.65% → 92.38%)
       │    └─► CAUSE: Compositional mix-shift (+8.0pp shift toward BOPIS/Pickup)
       │    └─► CAVEAT: Hardest channel (Ship-to-Home) actually declined (-0.20pp)
       │
       └─► COST PER ORDER: Down $0.55 structurally ($7.85 → $7.30 QTD)
            └─► CAUSE: DC sortation automation rollout at FON2 / JOL1
            └─► CAVEAT: Q4 spike ($8.60) masks pure run-rate via seasonal reversion
```

Conflating these two findings leads to poor strategic planning. If leadership assumes our ship-to-home shipping reliability is improving because our cost per order is falling, we will underinvest in the carrier-relationship management and line-haul optimization needed to actually move that 89.30% ship-to-home floor upward.

---

## 5. Confluence Discussion & Comments

> **`gabriel.stroud`** *(Fulfillment Ops Lead)* — 2026-07-21 09:14 AM  
> Spot on, Tara. Looking back at the FON2/JOL1 rollout logs from February, our sort throughput per man-hour went up roughly 24% once the automated sorters bedded in. But that mechanical gain speeds up throughput; it doesn't magically make UPS or FedEx trucks run faster down I-80 during a snowstorm. We shouldn't be surprised that ship-to-home OTP stayed flat while unit cost dropped. Good to have this explicitly documented so finance stops mixing them together.

> **`amara.shah`** *(Data Analyst)* — 2026-07-21 10:32 AM  
> Thanks for putting this together, Tara. Will reference this exact page in the upcoming Q3 MBR prep deck so we don't get the "automation improved delivery reliability" talking point into the board slides again. One minor note: make sure anyone querying the historical tables remembers that `fulfillment_speed_daily` is full-population aggregate grain, so the mix share calculations check out to 3 decimal places without needing to touch `fact_orders`.

> **`tara.oduya`** *(Director PM Speed)* — 2026-07-21 11:05 AM  
> @amara.shah - Agreed, added a explicit callout to `fulfillment_speed_daily` in the text. Let's make sure Leo sees this too before his next promise-window policy review.

---
### TODOs / Follow-Up Actions
* [ ] **`amara.shah`**: Update the internal Speed data dictionary snippet to explicitly link blended OTP changes to the BOPIS mix-share formula.
* [ ] **`tara.oduya`**: Brief Ben Tanaka (`assoc_100050`) on the ship-to-home OTP stagnation (-0.20pp) ahead of the August logistics sync, ensuring we don't rely solely on store pickup mix growth to mask delivery-rate flatlines.
* [ ] **`gabriel.stroud`**: Check if the JOL1/FON2 automation cost-per-order slope is leveling off in Q2FY27 QTD data or if there's additional headroom once Phase 2 rolls out later this year.

---
