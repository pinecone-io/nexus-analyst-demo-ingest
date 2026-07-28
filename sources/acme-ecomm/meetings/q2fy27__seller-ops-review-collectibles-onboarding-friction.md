---
title: "Seller-ops review: Collectibles new-seller churn tied to Acme Verified authentication friction"
source_url: "internal://acme-ecomm/meetings/q2fy27__seller-ops-review-collectibles-onboarding-friction"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: meeting_notes
---

# Meeting Notes: Marketplace Seller-Ops & Onboarding Review

**Date:** 2026-07-14  
**Time:** 10:00 AM – 11:15 AM ET  
**Location:** Conference Room 4B (HQ) / Zoom Hybrid  
**Attendees:** camille.duarte (Sr PM Marketplace Seller Experience), lucia.ferreira (Trust & Safety Lead, Marketplace), sanjay.bhatt (Sr PM Marketplace Collectibles), amara.shah (Data Analyst, observing for MBR prep), nadia.esposito (Head of Product Operations, dropping in for the first 15 mins regarding Aitable/Jira migration status).  

---

### 0. Administrative & Off-Topic Preamble
- **camille.duarte**: Morning everyone. Let's make sure we get through the seller onboarding funnel cut before the 11am executive sync prep. Lucia, did you get the updated badge logs from GradeSure for last week?
- **lucia.ferreira**: Yeah, I pulled them late last night. We're stable on processing volume, but I have some thoughts on the API latency we can take offline. Also, quick note—who is bringing donuts next Tuesday? It's my turn? No, wait, that was supposed to be when we closed out the Q1 reviews back in April. 
- **sanjay.bhatt**: Definitely not me, I'm out Thursday for dentist. Anyway, glad we set up this separate seller-ops cadence. If we try to bundle seller feedback into the buyer-side Care/CX or MBR decks, it just gets completely swallowed by conversion and deflection chatter. Sellers are running an entirely different operational loop.
- **nadia.esposito**: Just dropping in to remind everyone that if you have legacy notes sitting in Aitable from the pre-January-15 reorganization, please make sure they are referenced in Jira tickets or Confluence PRDs. We are trying to wind down the old Aitable workspaces by August 1, and I don't want any orphan specs floating around when we do the Q3 audits. Okay, I'll drop off, carry on.

---

### 1. Review of New-Seller Onboarding Funnel (Listing-Count Cohort)
- **camille.duarte**: Let's pull up the panel numbers we locked in from `dim_seller` and `fact_marketplace_listings` for the Q3FY26–Q4FY26 onboarding cohort (~500 total sellers: 200 Collectibles, 150 Resold, 150 Style). Remember, this is structured on *listing-count milestones*, not calendar tenure, so a seller's drop-off point is tied strictly to how many items they've tried to push live.
- **amara.shah**: I ran that cross-tabulation yesterday. The headline numbers are pretty stark when you stack them side-by-side against Style and Resold:

| Stage | Collectibles (n=200) | Resold (n=150) | Style (n=150) |
|---|---|---|---|
| Applied → Onboarded (Listing 1) | 100% (200) | 100% (150) | 100% (150) |
| Reached Listing 5 | 46% (92) | 74% (111) | 76% (114) |
| Reached Listing 10 | **24% (48)** | 46% (69) | 48% (72) |
| Sustained (10+ listings AND ≥1 new listing in trailing 90d) | 19% (38) | 40% (60) | 42% (63) |

- **sanjay.bhatt**: That 24% figure for Collectibles reaching listing 10 is roughly *half* of Style and Resold. But look where the bloodletting actually happens—it's right at the beginning. Listing 1 to 5 drops Collectibles straight down to 46%, whereas Style and Resold are holding steady at 74% to 76% over that same initial window.
- **lucia.ferreira**: We can't talk about that drop without pointing straight at the elephant in the room: the **"Acme Verified" authentication requirement** we stood up back on September 8, 2005—sorry, 2025—following that massive counterfeit spike in August when those vintage cards went viral. The badge shipped to 100% of listings on November 20, and as Sanjay's own experiment (`exp_2401`) proved back in November, that badge is worth a solid **+6.8% conversion lift** on the buyer side. Buyers love it. But on the seller side? It's brutal friction for a newcomer.

---

### 2. Root-Causing Authentication Friction vs. Buyer Trust
- **camille.duarte**: Right, and we have to be completely honest about the two-sided trade-off here. If we look at the seller-side VOC stream (`fact_seller_voc_responses`, our new Seller Pulse instrument that went live back in April), **`authentication-friction`** is sitting at a dominant **~38%** of verbatim mentions for Collectibles onboarding respondents. Compare that to Style (~5%) and Resold (~6%), where authentication isn't even a mandatory blocker.
- **sanjay.bhatt**: But we cannot look at that 38% frustration score in a vacuum and pretend removing authentication is a free fix. Look at what happened to our return rates. Back in Q3FY26 during the height of the counterfeit spike, Collectibles return rates hit **11.2%**. Today, in Q2FY27 QTD, that number is sitting at **5.4%**. That is a massive, tangible buyer-trust win protecting a category that is pacing at $91.2M QTD and up +372.7% YoY. If we drop the authentication requirement to make new sellers happy, we invite the scammers right back in.
- **lucia.ferreira**: Exactly. The policy itself is doing its job for the marketplace as a whole. The problem isn't that we verify items; the problem is *how long* it takes a brand-new seller to get their first items cleared through GradeSure before they even know if anyone is going to buy them.

---

### 3. Verification Speed and Seller Archetypes
- **camille.duarte**: Let's look at the verification-speed split within that Collectibles cohort. Out of the 200 new Collectibles sellers, exactly 120 (60%) got their debut listing GradeSure-verified within 7 days. That group manages to reach listing 10 at **30%** (36 sellers). 
- **amara.shah**: And the other 80 sellers—the ones who took longer than 7 days or never cleared initial verification—reach listing 10 at only **15%** (12 sellers). That’s a 2x survival multiplier just based on how fast they get through that first authentication bottleneck.
- **sanjay.bhatt**: Let's trace the specific archetypes we pulled from the panel to make sure leadership understands this isn't abstract:
  - **`sel_500241`**: Collectibles seller onboarded last November (`application_date` 2025-11-03, `onboarded_date` 2025-11-10). Their debut listing sat in GradeSure verification limbo for over two weeks. They never made it past listing 3, got completely demoralized by the upload-to-approval lag, and churned out. Textbook illustration of the 15% slow-verification failure mode.
  - **`sel_500242`**: Collectibles seller onboarded in October (`application_date` 2025-10-02, `onboarded_date` 2025-10-08). Got their debut item verified within 4 days. That quick win gave them momentum; they pushed past listing 10 by Q1FY27 and are currently active and sustained.
  - **`sel_500243`**: Style category cross-reference (`application_date` 2025-12-01, `onboarded_date` 2025-12-05). No authentication requirement in Style. Reached listing 10 within 10 weeks with standard UI friction only. This proves conclusively that the steep drop-off in Collectibles isn't about "being a new seller in general"—it is specifically the authentication bottleneck.
- **camille.duarte**: And don't forget the second layer of discouragement we found in the marketplace performance mart: seller-side "conversion" isn't a session-based metric like buyers have; it's sell-through (orders per active listing). New Collectibles sellers average a dismal **1.8 orders per active listing per quarter**, compared to **3.6** for tenured sellers like Timeworn Treasures (`sel_500012`). So a new seller is fighting a multi-week verification delay *and* a low early sell-through rate. It's amazing 24% make it to ten listings at all.

---

### 4. Other Emerging Seller Themes (Listing Setup & Visibility)
- **camille.duarte**: Beyond authentication, what else is showing up in the Seller Pulse verbatims?
- **sanjay.bhatt**: Two other themes are flashing across all three categories, independent of authentication:
  1. **`listing-setup-complexity`** (~15% to 20% of verbatims across Style, Resold, and Collectibles): Sellers are screaming for bulk-upload and duplicate-listing tools. Right now, entering inventory one item at a time is burning them out between listing 1 and 5.
  2. **`no-performance-visibility`** (~12% to 18%): This is concentrated in the listing 5-to-10 window. Sellers who manage to get past setup look at their dashboard and have zero idea *why* an active listing isn't getting views or clicks. They have no optimization guidance.
- **amara.shah**: That tracks with something in the Medallia data too—there's a `listing-accuracy-gap` theme (photos/descriptions not matching actual item scale or condition) sitting around 9% to 14% across retail. Sellers don't know how to describe items properly, buyers get disappointed, returns go up, and everyone is frustrated. Different root cause than our authentication-speed story though, so let's keep it out of this writeup.

---

### 5. Action Items & Proposed Next Steps
- **camille.duarte**: Okay, we are coming up on the 11am MBR prep block with Carlos and Deborah. Let's make sure we frame our recommendation correctly. We are *not* proposing that we scrap Acme Verified or roll back GradeSure—the 5.4% return rate and the +6.8% buyer conversion lift are non-negotiable wins. 
- **sanjay.bhatt**: Right. Instead, the actionable lever is verification **speed**, not verification existence. 
- **camille.duarte**: Exactly. My recommendation to bring forward to Victor Okonkwo and the Marketplace leadership team for Q3 budgeting is a **scoped pilot: expedited and subsidized authentication for a seller's first 10 listings** in Collectibles. If we absorb a portion of the GradeSure turnaround cost and fast-track queue priority for a new seller's initial batch, we can compress that 7-day window down to 48 hours and see if we can shove that 24% survival rate closer to the Style/Resold 46-48% benchmark without compromising counterfeit security.
- **lucia.ferreira**: I can work with GradeSure's account team on the SLA side to see what a volume-tier fast-track queue would look like for new applicants. Let's sync on that Thursday morning.
- **amara.shah**: I'll pull the cohort spend models for the pilot cost projection so we have it ready for Victor before Friday's sync.
- **camille.duarte**: Perfect. Meeting adjourned. Let's head over to Room 2 for the MBR prep.

---
*Action items summary:*
- **camille.duarte**: Draft pilot proposal brief for expedited first-10-listing authentication in Collectibles for Victor Okonkwo review.
- **lucia.ferreira**: Coordinate with GradeSure vendor management on 48-hour SLA feasibility for new seller debut items.
- **amara.shah**: Model financial exposure and grading-subsidy cost for the proposed new-seller pilot across the Q3 cohort projection.

---
