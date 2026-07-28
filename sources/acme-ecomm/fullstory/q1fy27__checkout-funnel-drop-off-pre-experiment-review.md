---
title: "FullStory session-replay note: checkout funnel drop-off review ahead of Checkout Simplify"
source_url: "internal://acme-ecomm/fullstory/q1fy27__checkout-funnel-drop-off-pre-experiment-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: fullstory_session_note
---

**Author:** owen.faust (Sr PM Checkout & Conversion, US_CONV, assoc_100111)  
**Review Period:** Early February 2026 (Synthesized from Q1FY27 checkout funnel replay audits)  
**Related Jira Epic:** `JIRA-4892` (Checkout Simplify prep)  
**Target Experiment:** `exp_2214` ("Checkout Simplify", kicking off 2026-02-16)  

---

### Executive Context & Qualitative Groundwork

Following up on the qualitative groundwork established during our Q2FY26 review (and carrying forward the insights from our ongoing optimization work across the US conversion funnel), my product squad pulled a fresh cohort of session replays in FullStory across the first week of February 2026. This review was deliberately scoped to examine user behavior right at the boundary of the cart-to-checkout transition, just ahead of the `exp_2214` ("Checkout Simplify") experiment kickoff slated for February 16, 2026. 

As we noted in our early product syncs with maya.lindqvist (US Conversion & Traffic) and felix.arroyo (SVP Product & Growth), site traffic has faced a structural headwind this quarter—most notably due to the 18% paid-search budget cut initiated on February 4 as part of martech's efficiency push (`camp_98214`). Because top-of-funnel volume is intentionally constrained, every single session that reaches our checkout funnel has to work harder. Unfortunately, these session replays confirm what our Medallia VOC verbatims have been hinting at: too many high-intent shoppers are hitting avoidable friction walls right when they try to pay.

This note documents the specific friction points our upcoming experiment variant addresses—specifically redundant form steps, legacy address-validation loops, and a remarkably opaque guest-checkout path that continues to suppress conversion across our desktop and mobile web experiences.

---

### Detailed Replay Observations: Friction Points

We reviewed roughly 250 session replays where users added items to cart (using `fact_traffic_daily` baselines as our denominator anchor) but abandoned prior to order placement (`fact_orders` drop-offs). The qualitative patterns cluster into three distinct failure modes:

#### 1. The Redundant Form Steps & Address Re-Entry Loop
In the legacy checkout flow, users who select standard ship-to-home are routinely forced through separate, sequential form views for shipping address, billing address, and payment method—even when the billing details match shipping identically. 
* *FullStory Behavior Signature:* In session re-plays (e.g., sessions originating from both web and mobile device filters), users frequently exhibit rapid mouse jitter or erratic scrolling between the "Shipping Address" and "Billing Address" form fields. In many replays, users encounter a soft validation error on the shipping line (such as a minor suite-number formatting mismatch caught by our legacy carrier validation service) which resets *both* address blocks, forcing manual re-typing.
* *Quant Link:* This maps directly to the drop-off spike we see between `checkout_started_sessions` and completed orders. Shoppers literally rage-quit the form. `exp_2214` ("Checkout Simplify") directly attacks this by collapsing shipping and billing into a single unified accordion step with a smart "Same as shipping" toggle enabled by default.

#### 2. The Unclear Guest-Checkout Entry Point
For non-member shoppers (or members who are not currently logged into their active session cookies, a common occurrence when switching devices or clearing browser data), the transition from the slide-out cart drawer to the primary checkout screen presents an ambiguous dual-CTA wall.
* *FullStory Behavior Signature:* Users land on `/checkout/auth` and hover dazedly between the prominent "Sign In to Acme+" login block and the understated, greyed-out guest email input field below it. In roughly 38% of guest-flagged abandoned sessions in our sample, the user clicks the sign-in button out of reflex, realizes they forgot their password, attempts a password reset, encounters friction, and abandons the site entirely rather than completing the purchase as a guest.
* *Strategic Alignment:* While our Acme+ membership team (led by simone.laurent and derek.holloway) continues driving great retention metrics on our 14.35M+ true member base, forcing non-members through a heavy login gate at checkout is an aggressive conversion tax. The Checkout Simplify variant replaces this dual-wall trap with a clean, email-first entry field that gracefully prompts for guest checkout while offering a low-friction "Already have an account? Tap to sign in" inline expansion.

#### 3. Mobile Device Field Misalignment & Keyboard Occlusion
With mobile sessions accounting for a growing share of our traffic mix (especially as we track weekly device mix shifts in our WBR packs), we paid special attention to mobile-web replays.
* *FullStory Behavior Signature:* On iOS Safari and Chrome Android, when the virtual keyboard pops up to collect credit card expiration data or CVV numbers, the fixed footer navigation bar and the sticky "Place Order" CTA block occlude the lower half of the input form. Users are forced to manually swipe down to dismiss the keyboard just to see what they typed, leading to frequent mis-entries and ultimate cart abandonment.

---

### Intersection with Broader Engineering & Data Notes

As wei.hartono reminded us during our last analytics engineering sync, anyone analyzing these conversion funnels must keep the upcoming `sessions_definition_version` 1→2 cutover (scheduled for March 2, 2026) in mind. While this session-replay review is qualitative and observational, our quantitative analysts (amara.shah, giulia.romano) need to ensure that pre- and post-cutover funnel drop-off metrics aren't conflated once the bot/crawler filtering and multi-tab de-duplication changes go live next month. 

Furthermore, we must coordinate closely with maya.lindqvist's team. Maya's Item Page Iteration Program (such as the above-fold price/CTA reflow that shipped on February 5, `v1`) is successfully driving users down to the cart; it would be tragic to feed high-intent traffic down from the product detail pages only to lose them in my checkout funnel because of legacy form bloat. 

Similarly, looking backward at the operational headaches our care and returns teams faced during peak (such as the Ontario, CA returns-center understaffing crisis that hannah.brennan and gabriel.stroud navigated through January and early February), we know that customer frustration often begins long before checkout. But checkout is where that friction translates directly into lost revenue. If a shopper has heard whispers about refund delays or return friction from peers, a cumbersome checkout form is all it takes to push them over the edge.

---

### Next Steps & Experiment Readiness

1. **Finalize Instrumentation:** Ensure FullStory event tagging for `exp_2214` variant assignments (`control` vs `simplify_v1`) is fully verified by connor.blake ahead of the February 16 launch date.
2. **Cross-Functional Alignment:** Share these replay snippets with the design and engineering pods supporting Owen Faust to reinforce *why* we are simplifying the form fields rather than just running a routine A/B test.
3. **Monitor Confounders:** Keep an eye on upcoming site-wide launches (such as the planned "Nav Refresh" sitewide navigation redesign scheduled for March 1, 2026) to ensure our checkout experiment readouts are properly isolated—or at least accounted for when we evaluate the final numbers in late March.

*Note on tooling:* As our Looker-to-Compass dashboard migration continues to settle, let's make sure these qualitative insights are linked directly to the `fact_experiment_exposures` metadata tables so future data analysts don't treat conversion drops purely as traffic anomalies when the UI form factors are playing such a heavy role.

---
