---
title: "FullStory session-replay note: buyer hesitation signals on unverified Collectibles listings"
source_url: "internal://acme-ecomm/fullstory/q3fy26__collectibles-listing-trust-signals-session-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: fullstory_session_note
---

# FullStory Session Review & Qualitative UX Notes: Collectibles Listing Trust & Verification UX

**Review Owner:** sanjay.bhatt (Sr PM Marketplace Collectibles)  
**Supporting Analysis Team:** UX Research & Behavioral Analytics (partnering with giulia.romano's VOC data group)  
**Date of Review Session:** 2025-10-15  
**Scope:** Session-replay observations on Collectibles category item pages, search results, and checkout funnels following the August counterfeit-listing spike and subsequent policy enforcement actions (including the suspension of high-profile actors such as Bramblewood Vintage on 2025-09-02, and the roll-out of the "Acme Verified" authentication partnership with GradeSure on 2025-09-08).

---

## 1. Executive Summary / Context

Following the viral vintage-card auction surge on August 4, 2025, and the subsequent operational emergency that flooded our Collectibles sub-vertical with an influx of unvetted listings and bad-faith actors (culminating in the Trust & Safety intervention led by lucia.ferreira and the temporary suspension of sellers like Bramblewood Vintage), our quantitative funnel metrics showed a sharp dip in visitor trust. Although the launch of the "Acme Verified" program with GradeSure on 2025-09-08 established a rigorous backend authentication check, front-end visual cues regarding listing authenticity remained highly inconsistent across legacy inventory versus newly onboarded items.

To understand why cart abandonment on high-value ungraded items ($150–$1,200 range) spiked by nearly 18% over the last six weeks—even as overall traffic to the Marketplace vertical remained elevated—we pulled and reviewed a random sample of 250 mobile and desktop session replays from users browsing Collectibles listings between October 1 and October 14, 2025. 

This qualitative session-replay review directly motivates the design and engineering rationale for expanding our active experiment space—specifically laying the behavioral groundwork for the prominent badge placement tested under `exp_2401` (the "Verified Badge Prominence" experiment started on 2025-10-01).

---

## 2. Key Behavioral Hesitation Patterns Observed

Across the 250 session replays analyzed, three distinct behavioral motifs emerged among buyers interacting with unverified or ambiguously badged Collectibles listings. These patterns almost never appeared in our Style or Resold categories during the same timeframe, pointing directly to category-specific anxieties around authenticity in high-value secondary market trading cards, vintage memorabilia, and rare currency.

### Pattern A: The "Listing & Seller Profile Ping-Pong"
* **The Behavior:** Users land on a high-value Collectibles product page from search results, scroll past the hero image, and immediately click the seller’s display name to open the seller profile sidebar or modal. They spend 15 to 45 seconds scanning the seller’s onboarding date, historical rating count, and past policy warnings. In roughly 62% of these instances, the user then clicks backward to the listing page, scrolls down to the Q&A / community comment section, clicks back to the seller profile, and then bounces entirely without adding the item to their cart.
* **FullStory Friction Metric:** Dead clicks on seller name anchors and excessive cursor jitter / erratic scrolling around the "Fulfilled by Seller" vs. "Acme Verified" metadata block.
* **Qualitative Takeaway:** Buyers are hunting for trust signals that aren't prominent enough in the viewport. Because the "Acme Verified" badge (launched 2025-09-08) was initially deployed as a small text footnote beneath the product description rather than an explicit badging overlay on the primary product thumbnail or buy-box, buyers cannot quickly verify if a listing has cleared GradeSure scrutiny without performing tedious reconnaissance on the seller's storefront history.

### Pattern B: High-Value Cart Abandonment Without Conversion Attempt
* **The Behavior:** Users add items priced above $250 to their cart (often rare sports cards or graded-alternative raw items) but exhibit prolonged hover/dwell times on the subtotal summary in the cart drawer. When comparing carts containing a mix of verified items (carrying the early GradeSure tag) and unverified items from newer merchants (such as items from our newer cohort nodes like sel_500202 or recent unvetted additions), users repeatedly toggle the item quantity or remove the unverified item entirely, proceeding to checkout with *only* the verified item, or dropping off the session completely.
* **FullStory Rage-Click / Hesitation Flag:** Repeated hovering over the informational tooltip icon ("What is Acme Verified?") next to certain items, contrasted with complete omission of tooltip interaction on items lacking any mention of verification.
* **Qualitative Takeaway:', The lack of a visible authentication badge on unverified or pending-verification listings is creating an implicit "lemons problem." Buyers treat *all* unbadged items as suspect in the wake of the August counterfeit spike and the Bramblewood suspension fallout, severely penalizing legitimate small sellers who haven't yet built up massive feedback loops.

### Pattern C: Image Zoom & Metadata Scrutiny Loop
* **The Behavior:** On unverified listings, users spend more than double the median time (averaging 74 seconds vs. 32 seconds on verified items) zooming in and panning across high-resolution product photos. They toggle back and forth between different listing photos looking for watermarks, certificate numbers, or slab serials, often opening browser developer tools or zooming to 300% on card corners—behavior that strongly signals skepticism regarding photo authenticity or stock-image usage.
* **FullStory Friction Metric:** Rapid pinch-to-zoom gestures on mobile web/app, followed by abrupt navigation away from the product detail page back to search results or vertical landing pages.

---

## 3. Operational & Organizational Noise / Cross-Team Chatter

* *Slack aside from amara.shah (Finance/MBR analyst) in `#marketplace-metrics`, 2025-10-12:* 
  "Hey team, are we seeing any weird anomalies in the Compass dashboard for Collectibles take rates this week? I noticed the Q4FY26 numbers are still showing that old flash-reported $952.4M figure in some cached executive views instead of the restated $975.0M we locked down after the returns-timing reclass. Let me know if you need me to force-refresh the BI mart connection before the MBR prep."
* *Internal coordination note regarding the ongoing T&S staffing:* 
  lucia.ferreira's team continues to process backlogs from the trust-and-safety overhaul. While the Bramblewood Vintage (sel_500089) case remains locked in suspension pending their formal compliance review (scheduled to run through the end of the quarter), new sellers onboarding into the collectibles vertical are facing strict queuing times with GradeSure. 
* *Lunch & office logistics:* 
  Reminder from office operations that the 3rd-floor pantry espresso machine is down for descaling until Thursday morning. Please use the 2nd-floor machine near the Data & Analytics bullpen (where wei.hartono and carlos.figueroa's teams sit).

---

## 4. Synthesis & Motivation for `exp_2401`

The qualitative signals documented in these session replays provide the foundational user-behavior rationale for sanjay.bhatt’s ongoing experiment (`exp_2401`, "Verified Badge Prominence," which kicked off in the Collectibles vertical on 2025-10-01). 

If buyers are forced to hunt through seller profiles and parse fine-print footnotes to determine whether a high-value item is authentic, conversion rates will remain suppressed regardless of how robust our backend GradeSure partnership is. By testing a prominent, above-the-fold visual badge directly on the product image thumbnail and buy-box (the core intervention of `exp_2401`), we aim to reduce the "Listing & Seller Profile Ping-Pong" friction loop, shorten the image-scrutiny dwell time, and safely recover checkout completion rates for legitimate Collectibles merchants.

We will review the quantitative readout of `exp_2401` upon its conclusion on November 15, 2025, alongside medaglia buyer verbatim reports from giulia.romano to evaluate whether the prominent badging successfully alleviates the trust deficit identified in these session replays.

---
