# Acme (eCommerce) — Demo Question Set

22 questions a PM would actually type into the always-on insights agent — 15 from
the original set (all kept; none conflicted with the sharpened spec) plus 7 new,
one per user story below. `CANON.md` exists to make every correct answer here
derivable, and every trap here real. Numbers are exact and cross-checked against
`CANON.md` — if a future document contradicts a number stated here, the document
is wrong, not this file.

**Framing that runs through all of it:** the customer's *customer* is the end
shopper; their *user* is the PM. A good answer carries both — shopper-outcome
language and PM-actionable output, at once. PM ownership is organized per
surface per vertical (view item page, search, seller listing, seller
optimization); Marketplace is a two-sided marketplace with buyer and seller as
separate orgs, separate KPIs, separate feedback loops; and the join the
customer can't do today is roadmap ledger ↔ metric movement ↔ voice-of-customer
— nearly every question below exercises some slice of that join.

Organized by the 7 user stories. Two are the demo's named centerpieces: **"the
masked trend"** (Q11, US-3) and **"the unstaffed blind spot"** (Q14, US-4).

## Coverage

| Story | Status | Questions |
|---|---|---|
| US-1 Metric movement → customer meaning | **new primary + kept** | Q1 (new), Q2, Q3, Q4, Q5, Q6 |
| US-2 Launch/roadmap attribution | **new primary + kept** | Q7 (new), Q8, Q9, Q10 |
| US-3 Experiments masking the trend | **new primary + kept** | Q11 (new — centerpiece), Q12, Q13 |
| US-4 Cross-vertical blind spot | **new, was missing** | Q14 (new — centerpiece) |
| US-5 Simple question, complex semantics | **new, was missing** | Q15 (new) |
| US-6 What next / prioritization | **new primary + kept** | Q16 (new), Q17, Q18, Q19, Q20 |
| US-7 Seller side | **new, was missing** | Q21 (new) |
| Foundational (not story-specific) | kept, lightly extended | Q22 |

See `CANON.md`'s new material for the full numbers behind every new question:
the weekly US Conversion detail and Item Page surface detail (under The
Numbers), the New-Seller Onboarding Funnel, the CROSS-VERTICAL BACKLOG
SNAPSHOT, and SIGNALS [offsetting-experiments], [item-page-metric-choice],
[roadmap-doesnt-explain-it], [listing-accuracy-blind-spot],
[seller-auth-friction].

---

# US-1 — Metric movement → customer meaning

"US conversion dropped — what happened, and what does it mean for the
shopper?" A good answer decomposes by segment, attaches the shopper-side
explanation from VOC, and distinguishes mix shift from real degradation. Q1 is
new (the live, weekly, VOC-attached version of this story); Q2-Q6 are kept —
each already exercises some part of "decompose before you believe the
headline," just without all three of Q1's ingredients (weekly grain, VOC
attachment, explicit mix-vs-real split) at once.

## Q1 — "Our US conversion number was down about 40 basis points last week versus the week before — what happened, and does it matter to customers?" *(new)*

**Use case:** US-1 (metric movement → customer meaning)

**Systems/tables joined:** `fact_traffic_daily` (weekly rollup, by `device`) ·
`fact_voc_responses` (Medallia, item-page-adjacent verbatims) ·
`dim_experiment`/`fact_experiment_readouts` (cross-reference only — see Q11).

**Correct answer:**
Blended US conversion fell from **3.24%** (week ending 2026-07-11) to **2.86%**
(week ending 2026-07-18) — **-0.38pp, "~40bps."** Decomposed (shift-share
basis): **-0.24pp is device mix-shift** — app's session share jumped
28.0%→37.6%, and app converts structurally lower than web (1.50% vs. web's
~4%), so a mix shift alone, with zero real behavior change, already explains
most of the move. That's not itself a customer-experience problem — it mostly
just reflects more sessions coming from a channel that converts differently.
The remaining **-0.14pp is a genuine, smaller web-conversion softening**
(4.00%→3.76%). Medallia verbatims tagged to item-page sessions in this exact
window skew toward the new autoplay media module feeling "cluttered" / "the
video just starts and it's annoying" / "page feels slower now" — low volume,
not yet a top theme, but the shopper-side texture for the real component.
Neither the shipped roadmap (Q7) nor the net effect of in-flight experiments
(Q11) explains the -0.14pp remainder — the honest answer says so rather than
forcing a tidy 100%-explained story onto it.

**Reasoning chain:** Pull the **weekly**, not quarterly, US conversion series
→ see the drop → pull device mix for the two weeks → find the app-share jump
→ recompute a counterfactual blended rate holding week-0 per-device rates
fixed, to isolate the mix effect → find it's the majority of the move →
isolate the smaller real/rate effect → pull Medallia verbatims scoped to
item-page sessions in the window → find the autoplay-carousel complaints →
attach shopper meaning to the real component → check roadmap and net
experiment effect for the remainder → find neither explains it → say so.

**The trap:** Reporting "conversion down 40bps, bad week" as one undifferentiated
number, and/or assuming the *entire* move is a customer-experience problem when
most of it is a mix artifact. The subtler, second-order trap: forcing the
small -0.14pp real remainder into a complete explanation (e.g., blaming it
entirely on the autoplay experiment, whose own documented effect, once diluted
by ~50% exposure, is smaller in absolute terms than that). The honest answer
holds a modest genuine softening *and* an honest "not fully explained" residual
at the same time.

---

## Q2 — "US conversion looked like it recovered last quarter — what actually happened?"

**Use case:** US-1 (what drove the metric movement + what it means for the customer)

**Systems/tables joined:**
`traffic_conversion_summary` (or raw `fact_traffic_daily`, filtered `market='US'`) for
the conversion/sessions/orders series · `dim_marketing_calendar` for the paid-search
budget-cut event · the `sessions_definition_version` column itself as the tell.

**Correct answer:**
Blended US conversion rose from 3.05% (Q1FY26) to 3.18% (Q1FY27), a +0.13pp move that
reads as a clean win — but it is not one. On 2026-03-02, Acme fixed session counting to
exclude bot/crawler traffic and de-duplicate multi-tab sessions
(`sessions_definition_version` 1→2), which mechanically raises measured conversion by
shrinking the denominator, independent of any real behavior change. The real story for
the quarter is on the traffic side, not conversion: US sessions fell **-5.6% YoY**
(402.0M → 379.5M) because of a deliberate **18% paid-search budget cut** (Martech,
Feb–Mar 2026, a company-wide marketing-efficiency initiative), and total orders fell
**-1.6% YoY** as a result (12.261M → 12.068M). Net: conversion "improved" mostly on
paper; real demand cooled because of a self-inflicted spend decision, not a customer-
experience or competitive problem.

**Reasoning chain:** Pull the quarterly conversion series → notice the up-move →
check `sessions_definition_version` on the underlying rows spanning the quarter →
see the 1→2 cutover mid-quarter and flag non-comparability → pull sessions and orders
(not just the rate) for the same window → see both down YoY → cross-reference
`dim_marketing_calendar` for a demand-side event in that window → find the paid-search
cut → conclude traffic, not conversion, is the real story, and even the conversion
number is partly definitional.

**The trap:** Reporting "conversion rate up 0.13pp, Q1 recovery" from the rate alone.
The planted fact that corrects it: the `sessions_definition_version` column plus the
explicit non-comparability note in `CANON.md`'s SIGNALS (session-definition change),
and the marketing-calendar entry for the spend cut.

---

## Q3 — "Is our delivery-speed number actually getting better, or is something else going on?"

**Use case:** US-1 (metric movement) — also touches experiments, but see the
note at the end of this entry.

**Systems/tables joined:**
`fulfillment_speed_daily` mart (blended and by-`fulfillment_type`) ·
`dim_marketing_calendar` (Pickup Perks campaign) · `dim_experiment`
(Wider Promise Window) · `fact_promise_vs_actual`.

**Correct answer:**
Blended on-time-to-promise (OTP) rose from 91.65% (Q1FY26) to 92.38% (Q1FY27),
+0.73pp — a headline win in the MBR deck. Decomposed by `fulfillment_type`,
ship-to-home (the majority-GMV, hardest channel) actually **declined slightly**,
89.50% → 89.30% (-0.20pp), over the same window. The entire blended improvement is
mix-shift: BOPIS/curbside ("pickup") share rose from 21.0% to 29.0% of orders
(+8.0pp), driven by the "Pickup Perks" discount campaign launched January 2026, and
pickup orders hit their promise ~99.6% of the time near-automatically (the promise
window itself is same/next-day and customer-triggered). Separately, the "Wider
Promise Window" experiment (`exp_1187`, 2026-01-12 to 2026-02-20) — which widened the
delivery estimate shown to customers — was confounded by a concurrent DC sortation
automation rollout at 2 DCs (FON2, JOL1) phased in over the same window: its
confounded full-window reading was +4.2pp OTP, but the deconfounded effect (isolated
to pre-automation volume) was only +1.5pp, alongside a real **-0.6%** conversion cost
from showing a less attractive promise — net negative, and it was killed 2026-03-02.

**Reasoning chain:** Pull blended OTP trend → see the improvement → decompose by
`fulfillment_type` before accepting the headline → see ship-to-home flat-to-down →
pull fulfillment-type mix shares for the same two quarters → see the pickup-share
jump → cross-reference the marketing calendar for a demand-side cause (Pickup Perks)
→ separately, check `dim_experiment` for anything live in Speed during the same
general period → find Wider Promise Window → check for concurrent launches at the
same DCs → find the automation rollout → separate the two effects.

**The trap:** Reporting "on-time-to-promise up 0.7pp, delivery is improving" from the
blended number alone, and/or citing the Wider Promise Window's confounded +4.2pp as
the clean causal effect of that specific test. The planted facts that correct it:
the `fulfillment_type`-level OTP columns in the mart (ship-to-home didn't move), the
mix-share columns (pickup share jump), and the DC automation timeline entry
overlapping the experiment window.

*Note on mechanism, not a change:* this is a **co-launch confound** (one experiment,
one concurrent automation program, entangled measurement) — mechanically different
from Q11's *offsetting pair* (two independent experiments, opposite signs, that
net to flat). Both are real, both stay in the corpus; don't conflate the two
mechanics if asked to compare them.

---

## Q4 — "Are there early warning signs in customer feedback that our dashboards haven't caught yet?"

**Use case:** US-1 (what it means for the customer) + a foundational
VOC-leads-quant precedent.

**Systems/tables joined:**
`fact_voc_responses` (Medallia, `theme_tag`) · the refund-cycle-time rolling metric
(Care/POR) · the returns-center staffing postmortem/timeline entry.

**Correct answer:**
Yes. The Medallia "refund delay" verbatim theme crossed **10%** share of
care-related verbatims (vs a ~3.5% baseline) the week of **2025-12-15** — a full
**3 weeks** before the quantitative 4-week-rolling `avg_refund_cycle_days` metric
crossed its own 5.0-day SLA alert threshold (week of **2026-01-05**, hitting 5.03),
and a full **7 weeks** before it was formally escalated at the **2026-02-02** Monthly
Business Review (the monthly review cadence, not the weekly rolling number, is what
triggered action). Root cause once escalated: the Ontario, CA returns-processing
center was running ~22% understaffed through peak because a hiring-freeze exception
that should have applied to it didn't — fixed shortly after the Feb 2 MBR, with the
rolling metric back to ~3.3 days by mid-March 2026.

**Reasoning chain:** Search Medallia verbatim themes for anything trending up in the
relevant window → find "refund delay" climbing from baseline in December → pull the
quantitative refund-cycle-days series for the same period → find its rolling average
crosses the alert threshold later → check when it was actually escalated
operationally (MBR cadence, not the raw metric-crossing date) → compute the lead time
→ pull the postmortem/timeline entry for root cause (Ontario staffing) to complete
the "what does it mean" half of the answer.

**The trap:** An agent that only looks at the quantitative metric will date the
"start" of the problem to early January or February and miss that VOC had already
flagged it in mid-December — understating how early this was knowable by ~7 weeks,
and potentially misdating the root-cause window if asked to correlate against the
(unrelated-timing) hiring-freeze policy change.

---

## Q5 — "Care contact deflection jumped this year — is that a good thing?"

**Use case:** US-1 (what drove the movement + what it means)

**Systems/tables joined:**
`care_deflection_daily` mart (deflection rate + CSAT by cohort) · `fact_care_contacts`
· `fact_voc_responses` (theme overlap with the refund-cycle incident from Q4).

**Correct answer:**
Partly. Deflection rose from 45.0% (Q4FY26) to 49.6% (Q1FY27) to 52.1% (Q2FY27 QTD),
and the multi-quarter trend coincides with the "Ask Acme v2" bot's rollout
(launched 2025-09-15) — though the attribution is inferential, not holdback-proven:
deflection was already climbing pre-bot (+2.3pp the prior quarter), the first full
quarter after launch gained less (+2.2pp, Q3→Q4FY26) than that pre-launch quarter
did, and the single largest jump (+4.6pp) lands Q4FY26→Q1FY27, four-plus months
after launch. But CSAT
among deflected contacts specifically **dropped** from 3.70 (Q4FY26) to **3.42**
(Q1FY27) during the exact window the returns-processing understaffing/refund-delay
problem (Q4) was live — a meaningful share of the Q1FY27 deflection number reflects
return-status inquiries being pushed to self-serve tracking that could not actually
tell the member when their refund was coming, not genuine self-service success.
Deflected-CSAT partially recovered to 3.55 by Q2FY27 QTD as the backlog cleared.
Net: rising deflection is real progress *and* was temporarily inflated by an
unrelated ops problem — the two must be read together.

**Reasoning chain:** Pull deflection-rate trend → see the rise → before calling it
unambiguously good, pull CSAT-among-deflected for the same quarters → see it move
*opposite* to deflection in Q1FY27 → cross-reference the timeframe against the
returns-center staffing incident (Q4) → recognize the overlap is not coincidental →
conclude the deflection number is directionally real but was temporarily
contaminated by a specific, dateable ops failure.

**The trap:** Citing deflection-rate-up as an unambiguous win without checking
deflected-CSAT in the same window — the two metrics moved in opposite directions for
several months, and only joining them (or reading the CSAT columns already sitting in
the same mart) catches it. A second trap: crediting the entire multi-quarter rise to
the bot without a holdback — deflection was rising before launch and the biggest
single jump lands months after it, so the bot's specific share can't be cleanly
isolated from this data alone.

---

## Q6 — "How does conversion in Canada and Mexico compare to the US this quarter?" *(control — no manufactured trend)*

**Use case:** US-1 (applied cross-market)

**Systems/tables joined:** `traffic_conversion_summary` / `fact_traffic_daily`,
filtered by `market`.

**Correct answer:**
Q2FY27 QTD: US **3.22%**, CA **3.12%**, MX **2.67%**. CA tracks close to the US
(slightly below, consistent with a smaller, mature market). MX runs meaningfully
lower across the *entire* 6-quarter window (roughly 2.5–2.7% throughout) — this is a
stable, structural market-maturity gap, not a new or worsening trend. MX conversion
has not been declining; it has simply always run lower than US/CA.

**Reasoning chain:** Pull conversion by market for the current quarter → see the
US > CA > MX ordering → check history for all three markets across all 6 quarters
→ confirm the MX gap is persistent and roughly constant, not widening → conclude
there is no new MX-specific problem to explain.

**The trap:** Over-interpreting MX's lower absolute conversion as a recent decline
or manufacturing a root-cause narrative (e.g., a fictitious competitive or macro
event) for a gap that `CANON.md` states plainly has been stable for all 6 modeled
quarters.

---

# US-2 — Launch and roadmap attribution

"Which of the things we shipped or are shipping is connected to this shift?" A
good answer ranks candidates by timing and surface overlap and is willing to
say "none of these explain it." Q7 is new (the explicit "none of these"
case — the original 15 never had one). Q8-Q10 are kept: each already ranks
launch candidates against a metric shift, they just don't include a true
negative result.

## Q7 — "Did anything we shipped or are shipping cause this conversion drop?" *(new)*

**Use case:** US-2 (launch/roadmap attribution) — companion to Q1.

**Systems/tables joined:** `dim_marketing_calendar` (Homepage Hero Banner
Refresh + the Item Page Iteration Program) · Jira/Aitable roadmap
(cross-reference against the CROSS-VERTICAL BACKLOG SNAPSHOT) ·
`fact_traffic_daily`.

**Correct answer:**
No. Checking the marketing calendar for the drop window (week of 07-11 to
07-18): the only launch is "Homepage Hero Banner Refresh" (2026-07-13) —
homepage-only, no item-page or search overlap, and a query-log/FullStory
review around it shows no measurable conversion effect. No other roadmap item
shipped in that window. Of the shipped-and-launched roadmap specifically,
**none of it explains this move** — the explanation lives elsewhere (device
mix-shift, plus a modest, not-fully-explained real softening — see Q1). This
is distinct from *in-flight experiments*, which are a different source and
are relevant, just not to the same degree the naive "check what launched"
instinct assumes — see Q11.

**Reasoning chain:** Pull `dim_marketing_calendar` for the drop week → find
Homepage Hero Banner Refresh as the only candidate → check its stated scope
(homepage vs. item-page/search) → check FullStory/query-log evidence for a
measurable effect → find none → check for any other Jira/Aitable roadmap item
completed or shipped in the window → find none → conclude the roadmap does
not explain this move, resisting the pull toward "something must be
responsible" reasoning that credits the nearest-in-time launch anyway.

**The trap:** Crediting the Homepage Hero Banner because "it launched right in
the window" — classic timing-only, no-mechanism reasoning. The planted facts
that correct it: the banner's explicitly stated scope (homepage-only) and the
explicit finding of no measurable effect in FullStory/query-log review.

---

## Q8 — "We ran a checkout redesign test this spring — did it work, and is it safe to keep rolling out?"

**Use case:** US-2 (launches connected to a shift) — also touches experiments;
see the mechanism note at the end.

**Systems/tables joined:**
`dim_experiment` (Checkout Simplify + Nav Refresh Holdback rows) ·
`fact_experiment_exposures` and `fact_experiment_readouts` · `dim_marketing_calendar`
(Nav Refresh launch date) · Confluence PRD for Nav Refresh (cross-reference).

**Correct answer:**
The Checkout Simplify experiment (`exp_2214`, 2026-02-16 to 2026-03-30, US market)
shows **+2.1%** conversion lift over its full window and shipped to 100% on
2026-04-06 on that number. But the sitewide "Nav Refresh" redesign launched into
**both** arms on 2026-03-01 — mid-experiment — and independently lifted conversion
~**+1.3%** sitewide (measured via its own 5%-of-traffic no-launch holdback,
`exp_2215`, held for 3 weeks). Everything in the readout after March 1 is confounded.
The clean, pre-confound slice (Feb 16–Feb 28 only) shows a smaller but defensible
**+0.8%** lift. The checkout simplification is very likely net-positive on its own
merits, so shipping was reasonable — but any forward projection of its impact should
use **+0.8%**, not the confounded **+2.1%** headline.

**Reasoning chain:** Pull the experiment readout → note the date range → check
`dim_marketing_calendar`/Confluence for any other launch inside that window
(same market, same or overlapping funnel step) → find Nav Refresh launched
2026-03-01, mid-test, to both arms → pull the Nav Refresh holdback readout to get
its independent effect size → recompute the checkout experiment's readout using only
the pre-launch sub-window → report the smaller, unconfounded number as the
defensible one, with the full-window number labeled contaminated.

**The trap:** Quoting +2.1% as "the checkout redesign's impact" in any downstream
planning number. The planted fact that corrects it: Nav Refresh's launch date falls
inside the experiment window, and its own holdback-measured lift (+1.3%) is large
enough that it, not the checkout change, explains most of the gap between the
pre-confound (+0.8%) and full-window (+2.1%) reads.

*Note on mechanism, not a change:* this is a **co-launch confound** — one
experiment plus one concurrent, same-direction launch, entangled measurement.
Mechanically different from Q11's *offsetting pair* (two experiments, opposite
signs, net to flat) — don't conflate the two if asked to compare.

---

## Q9 — "Cost per order in fulfillment has been dropping — what's driving that, and is it sustainable?"

**Use case:** US-2 (launches connected to a shift)

**Systems/tables joined:**
`fulfillment_speed_daily` (`avg_cost_per_order_usd`) · `dim_fulfillment_node` · the DC
automation timeline entry (same event referenced in Q3).

**Correct answer:**
Cost per order fell from **$7.85** (Q1FY26) to **$7.30** (Q2FY27 QTD), with the
steepest single-quarter drop (-$1.05) landing Q4FY26→Q1FY27, coinciding with the DC
sortation automation rollout at 2 DCs (FON2, JOL1; phased 2026-01-12 to 2026-02-15) —
the *same* rollout that confounds the Wider Promise Window experiment in Q3. Caveat:
Q4FY26 itself was the *only* quarter with a QoQ increase (+$0.90, ordinary peak/
holiday cost pressure), so part of the following drop is normal post-holiday
reversion, not automation alone — the two overlap in time and can't be fully
separated at quarterly grain. Net of that seasonal noise, the full 6-quarter decline
is still a genuine, durable efficiency gain, distinct from the on-time-rate story: two different things happened at the same DCs at the
same time — a real cost improvement (automation lowers cost-to-serve) and a
partly-artifactual speed improvement (mix-shift, per Q3). It is easy to conflate "the
DCs got better" with "delivery got better," when cost improved for real while
promise-hit-rate for the hardest channel (ship-to-home) did not.

**Reasoning chain:** Pull cost-per-order trend → see the steady decline → find the
steepest inflection lines up with the DC automation window → check whether the
preceding quarter (Q4FY26) was itself a seasonal cost outlier before crediting the
full drop to automation → find Q4FY26 was the only QoQ increase (peak/holiday cost),
so some of the rebound is ordinary reversion → confirm the automation rollout is the
same one flagged in Q3 as a confound for a *different* metric → separate "cost
went down for a real, durable reason" from "on-time-rate's improvement was mostly
mix-shift" — two distinct conclusions about the same underlying event.

**The trap:** Crediting the on-time-rate improvement (Q3) to the same DC automation
that genuinely drove the cost improvement here — conflating two metrics that moved
around the same time for different reasons (one real operational cause, one a
population mix-shift). A second, subtler trap: crediting the *entire* steepest QoQ
drop to automation without noticing the immediately preceding quarter (Q4FY26) was
itself an atypical peak-driven cost spike — some reversion was coming regardless.

---

## Q10 — "Give me a complete list of everything on the roadmap for Speed and Membership this half."

**Use case:** US-2 (roadmap prioritization / systems-integrity angle) — a
prerequisite check for any US-2/US-4 answer that needs a *complete* backlog.

**Systems/tables joined:** Aitable (legacy roadmap cards) · Jira (current roadmap
tickets) · Confluence (PRDs, both eras).

**Correct answer:**
A complete answer requires **both** Aitable and Jira. Roadmap items opened before
**2026-01-15** live in Aitable (legacy); items opened on or after that date live in
Jira. The two systems are mid-migration (a consolidation project kicked off
2026-01-15, not complete as of "today," 2026-07-20) — Confluence holds PRDs for items
in both eras, and can be used to cross-check completeness. A query against only one
ticketing system will silently return a partial roadmap. (The CROSS-VERTICAL BACKLOG
SNAPSHOT for Style/Resold/Collectibles/B2B, used in Q14, is deliberately built this
same way — both systems, enumerated completely.)

**Reasoning chain:** Attempt to pull "the roadmap" → notice the natural first
instinct is to query Jira only (the newer, more actively-referenced system) → check
whether an older tracking system exists → find Aitable, and the 2026-01-15 migration
cutover date → re-pull combining both sources → cross-check completeness against
Confluence PRDs, which span both eras.

**The trap:** Querying only Jira and presenting the result as "the roadmap" —
silently missing everything opened before mid-January 2026. The planted fact that
corrects it: the explicit migration-cutover date and the org announcement describing
the still-in-progress consolidation.

---

# US-3 — Experiments masking the trend

"Are any in-flight A/B tests contributing to or masking this?" A good answer
surfaces an offsetting pair — one lifting, one dragging, net ≈ flat — which is
invisible on an aggregate dashboard. Q11 is new and is the demo's **"masked
trend"** centerpiece; it uses a mechanic (two independent, opposite-sign,
concurrent experiments that cancel) deliberately distinct from Q8/Q3's
co-launch confounds. Q12-Q13 are kept.

## Q11 — "Are any of our in-flight tests contributing to or masking this?" *(new — centerpiece: "the masked trend")*

**Use case:** US-3 (experiments masking the trend)

**Systems/tables joined:** `dim_experiment` (`exp_2601`, `exp_2618`) ·
`fact_experiment_exposures` · `fact_experiment_readouts`.

**Correct answer:**
Yes — two, and they're masking each other, not the metric. Both started the
same day, 2026-06-08, and both are still running as of "today": "Search
Relevance Re-ranking" (`exp_2601`, **+1.6%** conversion lift on its exposed
arm) and "Item Page Media Carousel Autoplay" (`exp_2618`, **-1.5%** on its
exposed arm — a well-intentioned feature that backfired). Equal-weighted,
their blended net effect on the topline dashboard is **≈+0.05%** — essentially
a wash. A PM who checks only "net experiment effect" would see ~0% and
conclude nothing relevant is running — missing that two individually large,
real, opposite effects are live and canceling. Neither is the primary
explanation for the Q2FY27 weekly conversion drop in Q1 (that's mostly device
mix-shift); the autoplay experiment's negative arm is, however, the most
plausible source of Q1's smaller real-degradation component, and its
verbatim-level complaints ("cluttered," "annoying autoplay," "feels slower")
are visible in Medallia.

**Reasoning chain:** Query `dim_experiment` for anything running or recently
started in the relevant vertical/window → find **two**, not zero or one →
pull each readout independently → notice opposite signs → compute the
blended/equal-weighted net → recognize it's near zero → resist stopping there
— "net effect is ~0" and "nothing is happening" are different claims → report
both individual effects, since a near-zero net is exactly the shape that hides
two real things.

**The trap:** Computing only the net effect and reporting "no material
experiment impact" — technically the net figure *is* near zero, but the
correct behavior surfaces both individual, materially-sized effects
underneath. This is the demo's "masked trend": two things happening, mutually
invisible on the aggregate.

---

## Q12 — "Did the authentication-badge test on Collectibles listings actually move the needle?" *(control — clean result)*

**Use case:** US-3 (in-flight/recent experiments)

**Systems/tables joined:** `dim_experiment` ("Verified Badge Prominence") ·
`fact_experiment_readouts` · `fact_marketplace_listings`.

**Correct answer:**
Yes, cleanly. **+6.8%** conversion lift on Collectibles listings showing the
prominent "Acme Verified" badge, tested 2025-10-01 to 2025-11-15, no concurrent
launch or marketing event overlapping that window in Collectibles, shipped to 100%
2025-11-20. This is a deliberately uncomplicated, unconfounded result — and it's the
same authentication program whose new-seller-side friction cost shows up in Q21;
the two are not in tension (one is the buyer-side conversion effect during the test,
the other is an ongoing seller-onboarding cost the program carries afterward).

**Reasoning chain:** Pull the experiment readout → check for concurrent
launches/campaigns in the same vertical and window (the same check applied in
Q8/Q3) → find none → report the clean lift as-is.

**The trap (inverted):** Because several other experiments in this corpus
(Checkout Simplify, Wider Promise Window, and now the offsetting pair in Q11) are
confounded or paired, an agent that has learned "always find the catch" may
manufacture a caveat that doesn't exist here — hedging a clean result or inventing a
confound. The correct behavior is recognizing when a result really is clean and
saying so without qualification.

---

## Q13 — "The Membership team just ran a benefit-onboarding-carousel test — should we roll it out?"

**Use case:** US-3 (in-flight experiments) + informs US-6's prioritization.

**Systems/tables joined:** `dim_experiment` ("Benefit Onboarding Carousel") ·
`fact_experiment_readouts` · the benefit-adoption/renewal correlation from Q19.

**Correct answer:**
Ship it, but be precise about what is and isn't known yet. The test (2026-05-01 to
2026-06-15, still inside its full readout horizon as of "today," 2026-07-20) shows a
genuine **+9pp** lift in 30-day benefit awareness — a good leading indicator,
consistent with the Q19 finding that benefit-awareness is the highest-leverage CLTV
lever. But the outcome that actually matters for CLTV — annual renewal rate — cannot
be validly read for roughly 12 months per member cohort, so no renewal-rate readout
exists yet. Recommendation: ship (low-risk, aligned with an already-validated
mechanism), and explicitly flag that a renewal-rate claim isn't available until
roughly Q2FY28, when the first onboarded cohort reaches its 12-month mark.

**Reasoning chain:** Pull the experiment readout → see only a 30-day-window metric
is available (awareness) → check whether the primary business metric (renewal) has
had time to mature given the test's start date and the renewal cycle length →
conclude it hasn't → connect the available leading indicator to the already-validated
Q19 mechanism (awareness → adoption → renewal) to justify shipping despite incomplete
data → state the correct future date to revisit the outcome metric.

**The trap:** Either (a) refusing to recommend action because "the data isn't all
in yet" — overly conservative given a validated mechanism and a low-risk change — or
(b) fabricating/projecting a renewal-rate number that doesn't exist. The correct
answer holds both truths at once: act now, and don't claim a number that isn't
measurable yet.

---

# US-4 — Cross-vertical blind spot

"Are there patterns across verticals that no single PM would see?" Was
**missing** entirely from the original 15 — Q17/Q18 (formerly Q5/Q6) are
cross-vertical *within* Marketplace but never involve VOC themes or backlog
ownership, so they don't actually serve this story (see the gap analysis).
Q14 is new and is the demo's **"unstaffed blind spot"** centerpiece.

## Q14 — "Are there patterns across our verticals that no single PM would see because we're all just looking at our own numbers?" *(new — centerpiece: "the unstaffed blind spot")*

**Use case:** US-4 (cross-vertical blind spot)

**Systems/tables joined:** `fact_voc_responses` (`theme_tag = listing-accuracy-gap`,
across Style/Resold/Collectibles/B2B) · Jira/Aitable backlog per vertical (the
CROSS-VERTICAL BACKLOG SNAPSHOT, 20 items).

**Correct answer:**
Yes. A `listing-accuracy-gap` VOC theme (listing photos/descriptions not
matching true scale, condition, or specification) sits at a non-trivial,
roughly steady share (2-3 quarters flat, not a rising trend) in **all four**
of Style (14%), Resold (12%), Collectibles (9%), and B2B (22%, bulk-order
buyers hit by spec-sheet/pallet-configuration mismatches). Cross-checking each
vertical's *current, complete* backlog (5 items each, 20 total) shows **none
of them owns it** — it sits adjacent to several (Style's UGC-content pilot,
Resold's condition-grading rubric, Collectibles' badge-visibility expansion,
B2B's catalog API) without any of them actually addressing photo/description
accuracy. No one owns it today because each PM reads only their own vertical's
VOC report and backlog — the cross-vertical read is what's missing.
Recommended owner: camille.duarte (Sr PM Marketplace Seller Experience,
listings-side — the surface-based role, not a vertical-based one), sponsored
by victor.okonkwo (the only role spanning all three Marketplace
sub-verticals) for the Marketplace slice, coordinating with malik.hendon for
the B2B slice.

**Reasoning chain:** Pull VOC theme shares *per vertical* → notice something
non-trivial (not necessarily each vertical's #1 theme) recurring across
multiple, otherwise-unrelated verticals → pull each vertical's current
backlog in full → confirm none contains a matching item (check adjacent-
looking items specifically, since a near-miss is the realistic failure mode)
→ identify who's closest, using the *surface*-based org structure (surface
ownership crosses verticals; vertical PMs don't) → recommend an owner and a
sponsor.

**The trap:** Checking only one vertical's VOC + backlog (whichever the
question happens to name) and concluding either "minor, low share, not worth
flagging" (missing that it's the *pattern across verticals*, not any single
share, that matters) or wrongly crediting an adjacent-looking backlog item
with already covering it (e.g., assuming Collectibles' badge-visibility work
already handles this — it targets search placement, not photo/description
accuracy).

---

# US-5 — Simple question, complex semantics

"How did the item page do last quarter?" Was **missing** — no existing
question exercised the "state which definition and why" pattern at the
item-page surface, and there was no item-page metric, program, or mid-quarter
definition change in canon to ask about before this pass.

## Q15 — "How did the item page do last quarter?" *(new)*

**Use case:** US-5 (simple question, complex semantics)

**Systems/tables joined:** `fact_traffic_daily` (`product_view_sessions`,
`add_to_cart_sessions`, `sessions_definition_version`) · `dim_marketing_calendar`
(Item Page Iteration Program, v1-v6).

**Correct answer:**
Depends which metric you mean, and that has to be stated before answering.
**View-to-cart rate** (`add_to_cart_sessions/product_view_sessions`, an
engagement metric) went **18.0% → 19.9%** (+1.9pp raw) across Q1FY27.
**Item-page-scoped conversion** (`orders/product_view_sessions`) was **5.13%**
for the quarter — a *different, larger* number than the standard site
conversion rate (`orders/sessions`, 3.18%) because the denominator excludes
sessions that never reached a product page; neither is wrong, they answer
different questions. Both metrics inherit the **same**
`sessions_definition_version` 1→2 cutover (2026-03-02) that affects the
site-wide rate, because they're built from the same `fact_traffic_daily` row —
of view-to-cart's +1.9pp move, **≈+0.8pp is the same mechanical/definitional
bump**, **≈+1.1pp is real**, plausibly the Item Page Iteration Program (6
iterations shipped across the quarter, v1-v2 pre-cutover, v3-v6 post).
Silently averaging the whole quarter across the cutover overstates the real,
iteration-driven gain by roughly 40% relative.

**Reasoning chain:** Get asked a "simple" question → recognize that both "item
page" and "did well" need a definition before pulling anything → state which
metric(s) you're using and why → pull the raw quarterly figures → before
reporting, check whether a definitional change lands inside the quarter →
find the 03-02 cutover applies to these metrics too → split pre/post → assign
the raw move between mechanical and real → only then answer, caveat stated up
front, not buried at the end.

**The trap:** Answering with a single unqualified number (either metric)
without saying which one and why, and/or silently averaging the full quarter
across the version cutover — overstating the iteration program's real impact
by not accounting for the same measurement change that affects every other
session-based metric in this warehouse.

---

# US-6 — What next / prioritization

"What should I do next quarter, and what should I drop?" Q16 is new — a
synthesis question producing 3 ranked recommendations with evidence chains,
framed as planning input rather than a verdict. Q17-Q20 are kept: each is a
single, well-evidenced recommendation (Style/Collectibles headcount, the CLTV
lever, the FY27-goals read) that Q16 draws on as one ingredient of a larger
portfolio, rather than *being* the portfolio itself — that's the gap Q16 closes.

## Q16 — "Given everything we know, what should I actually prioritize next quarter — and what should I stop doing?" *(new)*

**Use case:** US-6 (what next / prioritization)

**Systems/tables joined:** draws on Q14 (cross-vertical blind spot), Q11
(offsetting experiment pair), Q19 (CLTV benefit-awareness lever), Q21 (seller
authentication friction), `member_cltv`.

**Correct answer:** Three ranked recommendations, each with its own evidence
chain and the metric it should move — framed as input to the planning ritual,
not a mandate:

1. **Fund a cross-vertical "listing accuracy" initiative**, owned by
   camille.duarte (Q14's finding) — expected to move Style/Resold/Collectibles
   return rate and the `listing-accuracy-gap` VOC share (currently 14/12/9%,
   plus B2B's 22%, the largest of the four).
2. **Kill or redesign "Item Page Media Carousel Autoplay"** (`exp_2618`,
   -1.5% conversion, real and significant — Q11) — expected to recover part of
   the real-degradation component in the weekly US conversion read (Q1). This
   is the concrete "what to stop."
3. **Launch a targeted streaming-benefit awareness push** (Q19's finding: 93%
   renewal among aware members, only 34% awareness) — expected to move Acme+
   annual renewal rate.

A fourth item is flagged as a **decision to make, not a recommendation
already reached**: the new-seller authentication-friction trade-off (Q21) —
Collectibles' Acme Verified requirement is simultaneously a proven buyer-trust
win (return rate 11.2%→5.4%) and a proven seller-acquisition drag (24% vs.
46-48% reaching listing 10). Removing it isn't free; a scoped pilot
(expedited/subsidized authentication for a seller's first 10 listings)
is the recommended next step to bring to the planning conversation, not a
unilateral call to make here.

**Reasoning chain:** Gather standing findings across verticals/signals rather
than pulling one new number → rank by evidence strength + expected impact +
effort → for each, state the metric it should move and how you'd know it
worked → explicitly separate "recommendation" from "trade-off needing a
decision" for the authentication-friction item rather than silently picking a
side.

**The trap:** Giving one "big swing" recommendation instead of a ranked
portfolio; presenting the output as a verdict/mandate rather than as planning
input; or silently resolving the authentication trade-off (either "rip it
out" or "leave it alone") instead of surfacing it as a genuine two-sided
trade-off that needs a decision.

---

## Q17 — "Marketplace's Style category is decelerating — is this a Style problem?"

**Use case:** US-6 (cross-vertical read feeding a prioritization call, via Q18)

**Systems/tables joined:**
`marketplace_gmv_summary` mart (Marketplace GMV by sub-vertical, full population) ·
`fact_marketplace_listings` (category attribute on Resold listings) · Marketplace
FY27 goal (Company section).

**Correct answer:**
No. Style GMV grew **+6.1% YoY** in Q1FY27 (vs. an ~10% planned/trend rate) — which
looks like a Style-specific demand problem from the Style dashboard alone. But Resold
GMV accelerated to **+90.9% YoY** over the identical window, and the share of Resold
GMV that is apparel/style-adjacent rose from **51% (year-ago) to 62%** (Q1FY27) —
strong evidence of a wallet-share shift toward resale, not a departure from Acme's
marketplace. Total Marketplace GMV is healthy and pacing at **117%** of its FY27
goal. The pattern only appears when Style and Resold are read together; neither
sub-vertical's own dashboard shows it in isolation.

**Reasoning chain:** Pull Style GMV YoY → see the deceleration vs. plan → check
whether total Marketplace (all three sub-verticals) shows the same deceleration →
find it doesn't (117% of goal) → look for where the "missing" Style growth went →
check Resold's growth rate and category mix → find the apparel-adjacent share climb
→ conclude it's a within-marketplace reallocation, not a demand loss.

**The trap:** Scoping the investigation to Style-only tables/dashboards and
concluding a real, isolated demand problem exists. The planted facts that correct
it: Resold's YoY acceleration in the same window, its category-mix shift toward
apparel, and total Marketplace's healthy pace-to-goal.

*Note:* this is cross-vertical *within* Marketplace (Style ↔ Resold), and
doesn't involve VOC or backlog ownership — it's a related muscle to Q14, not
US-4 coverage itself (see the gap analysis).

---

## Q18 — "Trust & Safety wants headcount for Collectibles fraud review, and the Style team wants headcount to investigate their slowdown. Who should get it?"

**Use case:** US-6 (roadmap prioritization, using Q17's cross-vertical read)

**Systems/tables joined:**
`marketplace_gmv_summary` mart (Collectibles GMV scale + YoY) ·
`fact_marketplace_listings` (`authenticity_verified` flags, return rate by category)
· `fact_care_contacts` (contact volume tagged to Marketplace/Marketplace categories)
· the Style/Resold finding from Q17 · Jira/Aitable (the two headcount asks) ·
Confluence (the abandoned "Style Conversion Recovery Plan" draft).

**Correct answer:**
Collectibles. Its return rate spiked to **11.2%** at the peak of the counterfeit
problem (Q3FY26, right as the category boomed) before the "Acme Verified"
authentication program (launched 2025-09-08, partnered with GradeSure) brought it
down to **5.4%** by Q2FY27 — Trust & Safety capacity there is protecting a rapidly
scaling GMV base (Collectibles is now $100M+/quarter, +372.7% YoY off a small base).
The Style slowdown, per Q17, is not an execution problem inside Style — it's a
wallet-share shift to Resold — so headcount aimed at "fixing Style demand" solves
the wrong problem. A draft "Style Conversion Recovery Plan" (Confluence, Q1FY27)
proposed exactly that reallocation before the cross-category read superseded it;
it was never actioned. Recommendation: fund the Trust & Safety ask; redirect the
Style team's request toward jointly instrumenting Resold's category mix rather than
an independent Style-only investigation. (Note the same Trust & Safety program has a
real seller-side cost too — see Q21 — worth weighing alongside this ask, not against it.)

**Reasoning chain:** Pull Collectibles return-rate history → see the spike-then-
recovery bracketing the Acme Verified launch → confirm Trust & Safety headcount is
protecting continued category growth, not firefighting a solved problem → re-derive
the Style situation from Q17 → recognize the Style ask is based on a premise (isolated
demand problem) that the cross-vertical data already falsifies → check Confluence/
Jira for any existing recommendation on this exact question → find the abandoned
draft that got the allocation wrong → recommend against repeating it.

**The trap:** Splitting the headcount evenly between the two asks, or defaulting to
Style because its absolute GMV is larger — both read as "balanced" without the
cross-vertical read, but the Style ask is solving a problem that (per Q17) isn't
actually a Style problem.

---

## Q19 — "What's actually the biggest lever we have to improve Acme+ member lifetime value?"

**Use case:** US-6 (a CLTV-side input to the ranked-recommendations synthesis)

**Systems/tables joined:**
`member_cltv` mart · `fact_membership_events` (`benefit_redeemed` rows, joined to
benefit code) · renewal rate by benefit-adoption-depth cohort.

**Correct answer:**
Benefit-adoption depth is the strongest lever: members using **2+** benefits renew
at **95%** annually vs. **71%** for members who only use free shipping. The single
strongest *individual* benefit is the streaming bundle (Vidora through 2026-05-31,
Reelstream since) — **93%** annual renewal among members who use it alone, on par
with the 2+-benefit cohort — but only **34%** of members are even aware they have
it. That 93% is a category-level read across both partner eras; Reelstream itself
has been live only 7 weeks and has no independently validated renewal read of its
own yet. The highest-leverage, lowest-effort
move available is a streaming-bundle awareness push, not a new benefit or a price
change. (Side note the agent should also get right if asked for "the number": mart
average CLTV is **$500/member**, not $625 — see Q20.)

**Reasoning chain:** Pull renewal rate cross-tabulated by benefit-adoption-depth →
see the steep 71%→89%→95% gradient → break the 1-benefit cohort down by which
specific benefit → find streaming-bundle-only users over-index at 93% → check
awareness/adoption rate for that specific benefit → find only 34% know they have it
→ conclude the fastest lever is awareness, not product.

**The trap:** Recommending a generic "add more benefits" or "run a broad renewal
discount" answer instead of the specific, cheap, targeted move the adoption-depth
breakdown actually supports. A subtler trap: quoting the mart's naive average CLTV
($625) as evidence without checking how it's computed (see Q20) — the corrected
figure ($500) and the population it hides (Q20) is itself part of the "signal to
improve CLTV" story, since the dormant population is unrealized value.

---

## Q20 — "Is Acme+ on track to hit its FY27 goals?"

**Use case:** US-6 (CLTV signals feeding "what's actually healthy")

**Systems/tables joined:**
`dim_member` (panel + true base), `member_cltv` mart (dormant-member count), Company
FY27 goals (member count, renewal rate targets), `fact_membership_events` (net-adds
pacing).

**Correct answer:**
Yes, on the headline: **14.62M** members at Q2FY27 QTD, pacing to **~15.05M** by
FY27-end (2027-01-31) against a **14.8M** target (~102%, AHEAD); renewal rate
**87.2%** vs. an **86.0%** target (BEAT). But `member_cltv` shows **20%** of the
member panel (24,000 of 120,000) had **zero orders** in the trailing 12 months —
still-active, still-paying, but dormant. These members don't hurt the headline
count or renewal-rate goals at all (they haven't cancelled), so goal-tracking alone
is structurally blind to them — they represent unrealized GMV and a real, silent
churn-risk population that "on track" would otherwise fully paper over.

**Reasoning chain:** Pull member count and renewal rate vs. their FY27 targets →
confirm both ahead of goal → don't stop there — check `member_cltv` for the
dormant-member share → find 20% with zero trailing-12mo orders → recognize this
population is invisible to both headline goals (they count as active members and as
non-churned for renewal purposes) → flag the gap between "hitting the stated goals"
and "the membership base is fully healthy."

**The trap:** Answering "yes, ahead on both metrics, no concerns" — technically true
but incomplete. The planted fact that corrects it: the dormant-member figure lives
only in the CLTV mart, not in the count/renewal metrics used for goal-tracking, so a
goals-only read cannot surface it.

---

# US-7 — Seller side

"Why are new marketplace sellers churning before their tenth listing?" Was
**missing** entirely — no existing question touched the seller-onboarding
funnel, seller-side VOC, or listing-quality signals. Built as a first-class
story: a real listing-count-based funnel, a fully separate seller-side VOC
stream, and a genuine two-sided tension tied to the *existing* Acme Verified
program rather than a parallel invented cause.

## Q21 — "Why are new marketplace sellers churning before they get to their 10th listing?" *(new)*

**Use case:** US-7 (seller side)

**Systems/tables joined:** `dim_seller` (`application_date`, `onboarded_date`,
`status`) · `fact_marketplace_listings` (`status`, `authenticity_verified`) ·
`fact_seller_voc_responses` (seller-side VOC — a separate stream from buyer
Medallia) · `marketplace_seller_performance` (seller-side "conversion").

**Correct answer:**
It's category-specific, not a universal new-seller problem. In the
listing-count-based funnel cohort (500 sellers, onboarded Q3FY26-Q4FY26, old
enough to have had time to reach listing 10), Style and Resold new sellers
reach listing 10 at **48%** and **46%**; Collectibles new sellers reach it at
only **24%** — half the rate — with the steepest relative drop-off happening
earliest (listing 1→5: **46%** for Collectibles vs. **74-76%** for
Style/Resold). Root cause, tied to canon already in place rather than a new
one: the **"Acme Verified"/GradeSure authentication requirement** (launched
2025-09-08, badge shipped 100% 2025-11-20, itself proven worth **+6.8%**
buyer-side conversion — Q12) is a genuine buyer-trust win (Collectibles return
rate 11.2%→5.4%) that also adds real per-item friction only new/small
Collectibles sellers feel in full — established sellers have amortized
workflows around it. Seller-side VOC (a fully **separate** stream from buyer
Medallia — different instrument, different cadence, different themes)
confirms it: `authentication-friction` is the dominant theme (~38%) among
Collectibles onboarding-pulse respondents vs. ~5-6% for Style/Resold. Sellers
whose debut listing gets GradeSure-verified within 7 days clear listing 10 at
**2x** the rate of those who don't (30% vs. 15%) — verification *speed*, not
verification itself, is the actionable lever. Two category-agnostic themes
(`listing-setup-complexity`, `no-performance-visibility`) are present at
similar levels across all three categories and explain some of the
non-Collectibles baseline churn too — they map onto the seller listing and
seller optimization surfaces respectively (owner: camille.duarte). Separately:
Collectibles new sellers (first 90 days) also sell through more slowly (1.8
orders/active listing/quarter vs. 3.6 for tenured Collectibles sellers) — a
second, reinforcing discouragement alongside the friction story. This is a
genuine two-sided trade-off (see Q16): removing the requirement would undo a
real, measured buyer-trust win, not a free fix.

**Reasoning chain:** Define the funnel by **listing count**, not calendar
tenure → pull survival by category → find Collectibles structurally worse at
every stage → check seller-side VOC (separate from buyer VOC) for a
category-specific theme → find `authentication-friction` dominates only in
Collectibles → tie the cause to the existing Acme Verified/GradeSure timeline
rather than inventing a new one → check the verification-speed split → find
the 2x relationship → check seller-side "conversion" (sell-through) as a
second contributing angle → state the buyer-side payoff too, framing the
whole thing as a real trade-off rather than a one-sided bug.

**The trap:** Treating "new sellers churn" as one undifferentiated,
population-level problem — missing the sharp category difference — or
recommending simply removing the authentication requirement without weighing
the proven buyer-side return-rate benefit it purchased. A second trap:
reaching for buyer-side Medallia data to explain a seller-side problem — the
two VOC streams are separate by design and must not be blended. A third,
KPI-definition trap: if asked for "Collectibles' seller conversion rate,"
answering with the buyer-side `orders/sessions` figure instead of
listing→sale (sell-through) — the two "conversion" concepts are not
interchangeable depending on which side of the marketplace is asking.

---

# Foundational (not tied to one user story)

## Q22 — "What's our total Acme+ membership base, and is that number reliable?"

**Use case:** foundational data-integrity question, relevant to any story that
touches a panel/sample table (which by now is most of them — see below).

**Systems/tables joined:** `dim_member` · Company section FY goals/actuals.

**Correct answer:**
The true active Acme+ base is **~14.62M** (Q2FY27 QTD), pacing toward **~15.05M** by
FY27-end vs. a 14.8M target. The `dim_member` **table** itself holds only **120,000**
rows — a representative panel (~0.82% sample of the true base) built for
cohort/CLTV/benefit-adoption analysis. `COUNT(*)` on `dim_member` is **not** the
total membership count and must never be reported as such; the true company-level
total comes from the membership system's own ledger (reflected in the Company
section's stated figures and MBR decks), never by resumming a panel table.

**Reasoning chain:** Asked for "total membership," the naive move is
`SELECT COUNT(*) FROM dim_member` → get 120,000 → recognize this is implausibly small
for a company at Acme's stated scale → check the table's documented purpose
(representative panel, not the ledger) → pull the true figure from the Company
section / membership system instead.

**The trap:** Reporting "120,000 Acme+ members" as the answer — confusing the
analytical panel with the true population. This is the single most structurally
important gotcha in the schema: every entity/event-grain table in this warehouse
(`dim_member`, `dim_seller`, `fact_orders`, `fact_care_contacts`,
`fact_voc_responses`, `fact_marketplace_listings`, `fact_membership_events`, and now
`fact_seller_voc_responses` and the new-seller funnel cohort within `dim_seller`) is
a panel, not a census, and the same mistake is possible on any of them.
