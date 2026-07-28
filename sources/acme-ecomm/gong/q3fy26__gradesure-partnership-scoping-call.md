---
title: "Gong call transcript: GradeSure partnership scoping call"
source_url: "internal://acme-ecomm/gong/q3fy26__gradesure-partnership-scoping-call"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: gong_call
---

# Gong Call Recording: Acme x GradeSure Partnership Expansion & Scoping
**Date:** 2025-08-25  
**Duration:** 48 minutes  
**Participants:**
- **Lucia Ferreira** (Trust & Safety Lead, Marketplace, Acme)
- **Sanjay Bhatt** (Sr PM Marketplace Collectibles, Acme)
- **Marcus Vance** (VP of Partnerships, GradeSure)
- **Sarah Lin** (Solutions Architect, GradeSure)
- **Dave Miller** (Account Executive, GradeSure)

---

### [00:00:00] -- Small Talk & Audio Check

**Dave Miller (GradeSure):** Hey everyone, can you hear me okay? Just waiting on Marcus to dial in from the Chicago office. The Wi-Fi here has been acting up all morning since they rolled out those new guest portal certs. How's weather in Seattle, Lucia?

**Lucia Ferreira (Acme):** Grey and wet, Dave, right on schedule. Sanjay's here with me too in the conference room. Sanjay, can you check if the projector audio is actually picking up? We've got our architecture team listening in async.

**Sanjay Bhatt (Acme):** Yeah, mic check, looks green. Morning Marcus, morning Sarah. 

**Marcus Vance (GradeSure):** Morning team. Sorry I'm a minute late, had an issue with a courier trying to drop off an ungraded slab at reception. Anyway, appreciate you setting this up. Following up on everything that happened earlier this month—especially with that viral vintage-card auction surge on August 4th—we wanted to present a concrete framework for scaling up our integration ahead of the Q4 holiday crush.

**Lucia Ferreira (Acme):** Perfect. Let’s dive straight in. As you know, since that counterfeit spike hit our Collectibles sub-vertical a few weeks back, leadership has been hyper-focused on tightening our verification loops. We want to make sure whatever we roll out for the September 8th launch date is rock solid and doesn’t create an unmanageable bottleneck for incoming sellers.

---

### [00:00:14] -- Intake Hubs & Physical-to-Digital Linking

**Sarah Lin (GradeSure):** Right. Let’s look at the intake architecture first. We’ve mapped out three primary models for handling the physical cards and high-value memorabilia before they hit your fulfillment network or direct seller shipping queues. 

**Sanjay Bhatt (Acme):** Before you share slides, let’s clarify the threshold. Our current spec with the engineering team is targeting anything listed above $250. Is your intake hub network equipped to handle direct-to-hub routing for those items without choking our sorting centers?

**Sarah Lin (GradeSure):** Yes, exactly. For items over $250, the seller won't ship directly to the buyer or to an Acme DC. They'll route through one of our three regional hubs—Dallas, Secaucus, or Reno. Once our authenticator inspects and slabs the item, we generate a secure cryptographic digital certificate linked directly to the `listing_id` in your marketplace database via our webhook API.

**Marcus Vance (GradeSure):** That linking mechanism is key. It ensures that when a buyer lands on a Collectibles PDP, the "Acme Verified" badge isn't just a static image asset; it’s dynamically queried from our verification ledger. If a listing is suspended or flagged later—like what happened with that Bramblewood Vintage account review we did last month—the badge status updates instantly.

**Lucia Ferreira (Acme):** That’s essential. We cannot have stale badges lingering on active listings if a seller gets flagged for compliance issues. Now, walk me through the SLA on turnaround time once an item hits your hub. Sellers are already grumbling about listing setup complexity; if your hub sits on a high-value card for a week, they’re going to churn out to eBay or MyCardPost.

**Sarah Lin (GradeSure):** Right now, our standard SLA for authenticated turnaround at the hub is 48 hours from receipt to digital cert generation. During peak Q4—say, November through December—we’re staffing up to maintain a 72-hour max ceiling. Anything past 72 hours triggers an automated escalation to our operations desk.

---

### [00:00:27] -- Pricing, Commission Structures, and Rev-Share

**Dave Miller (GradeSure):** Let’s talk commercial terms, because we’ve structured this to scale with your volume. Currently, for standard items, we’re proposing a tiered per-item authentication fee absorbed either by the seller or split via a platform subsidy, plus a modest SaaS platform fee for the API gateway integration.

**Sanjay Bhatt (Acme):** Walk us through the exact fee schedule for the $250-plus tier. Remember, our marketplace take rate across the board is sitting right around 13.6% right now, and we don't want to squeeze seller margins to the point where they abandon the platform entirely, especially since our new-seller onboarding funnel in Collectibles is already seeing higher drop-off at early listing milestones.

**Dave Miller (GradeSure):** Totally understood, Sanjay. Here’s the proposal: For items priced between $250 and $1,000, the flat authentication fee is $15 per item, which includes the physical slab, insurance during transit, and the digital cert linking. For items between $1,000 and $5,000, it’s $35. For anything above $5,000, it’s a 0.75% value-based fee. 

**Marcus Vance (GradeSure):** And on the rev-share side, GradeSure is willing to cede a 1.5% commission rebate back to Acme on every authenticated transaction to help offset your customer service and fraud-review overhead. 

**Lucia Ferreira (Acme):** 1.5% rebate helps, but let’s look at who bears the cost of return shipping if an item fails authentication at the hub. In our initial draft notes from the T&S team, we saw too many edge cases where sellers shipped counterfeit or misrepresented items, and someone had to pay to ship it back.

**Dave Miller (GradeSure):** If it fails authentication outright—meaning it’s flagged as a definitive counterfeit—return shipping back to the seller is charged at cost to the seller, plus a $10 processing penalty to deter bad actors from using your platform as a testing ground for fakes. If it's a minor condition discrepancy where the buyer and seller disagree, that's handled under Acme's standard marketplace dispute policy.

---

### [00:00:39] -- Rollout Timeline & Go-Live Contingencies

**Lucia Ferreira (Acme):** Okay, that penalty structure works for us. It aligns with our Trust & Safety enforcement guidelines. Let’s look at the calendar. Today is August 25th. Our hard launch date for the Acme Verified program across the Collectibles category is locked for September 8th. That gives us exactly two weeks to finish the API integration, test the webhook sync for the digital certs, and brief the account management teams.

**Sarah Lin (GradeSure):** The API endpoints are already staged in your lower environments. Connor Blake’s data engineering team ran initial ingestion tests last Thursday without errors, though they did flag a minor schema alignment issue with the `fact_marketplace_listings` table structure—something about matching the `authenticity_verified` boolean field correctly.

**Sanjay Bhatt (Acme):** Yeah, Connor mentioned that in the Slack channel. He sorted it out by Friday afternoon. The bigger risk isn't the API; it's seller communication. If we roll this out on September 8th without giving our top sellers—guys like Timeworn Treasures and the rest of the cohort—clear documentation on how to route their inventory to your hubs, we’re going to get hammered with support tickets.

**Lucia Ferreira (Acme):** Agreed. I’ll coordinate with Camille Duarte once she joins the seller experience side to draft an onboarding bulletin. We’ll make sure it goes out to all active Collectibles sellers by September 2nd so they have a full week to prep their shipping workflows before the badge requirement goes live.

**Marcus Vance (GradeSure):** We’ll provide a dedicated technical support alias on our end, too, so your CS agents don't have to troubleshoot GradeSure logistics manually. Our engineers will be on standby 24/7 during launch week.

**Lucia Ferreira (Acme):** Perfect. Thanks, Marcus. Let’s lock in the follow-up technical sync for Thursday morning to review the staging environment dry run. Sanjay, make sure you loop in Wei Hartono so we have analytics sign-off on the tracking events before we go live.

**Sanjay Bhatt (Acme):** Will do. Thanks everyone, talk on Thursday.

---
*(Call ended at 00:48:12)*
