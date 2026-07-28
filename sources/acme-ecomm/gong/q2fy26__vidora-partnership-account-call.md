---
title: "Gong call transcript: Vidora partnership account-management call"
source_url: "internal://acme-ecomm/gong/q2fy26__vidora-partnership-account-call"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: gong_call
---

# Gong Call Transcript

**Call Title:** Acme x Vidora Monthly Account Sync
**Date:** July 15, 2025
**Participants:**
- **Acme:** Renee Kowalski (SVP Membership), Derek Holloway (Sr PM Membership Benefits & CLTV), Amara Shah (Data Analyst)
- **Vidora (Vendor):** Greg Miller (VP Partner Management, Vidora), Sarah Chen (Account Director, Vidora), Marcus Vance (Technical Integration Lead, Vidora)
- **Duration:** 45 minutes
- **Platform:** Zoom / Gong Recording ID: `rec_vidora_q2fy26_0715`

---

**[00:00:12] Greg Miller (Vidora):** Hey everyone, good to see you. Renee, how are you holding up with the summer rush? I know you guys had a massive sprint around the streaming perk rollout at the start of June.

**[00:00:24] Renee Kowalski (Acme):** Hi Greg. Yeah, it's been pretty wild, honestly. Between managing the member acquisition targets and stabilizing the post-launch traffic, we've barely come up for air. But things are settling into a rhythm now. Good to see you too, Sarah, Marcus. 

**[00:00:41] Sarah Chen (Vidora):** Good to see you as well, Renee. And yeah, congratulations on the June 1st launch. Looking at our internal dashboard on this end, the initial redemption volume has been really encouraging. We wanted to use this check-in to walk through the technical integration health metrics for the first six weeks, talk through early redemption numbers, and give you an advance look at the content catalog refresh we're pushing out on our side next month.

**[00:01:15] Derek Holloway (Acme):** That sounds great, Sarah. From our side, we're definitely eager to see how the engagement cohorts are shaping up, especially since we're tracking member renewal rates very closely this quarter. Amara, did you pull those early streaming adoption numbers from the `fact_membership_events` mart before the call?

**[00:01:38] Amara Shah (Acme):** Yes, I did, Derek. Through the first six weeks post-launch, we're seeing roughly 34% of active Acme+ members activate or interact with the Vidora benefit at least once. That matches pretty closely with what we anticipated for phase one, though awareness is still something we're working on improving across the board.

**[00:02:05] Greg Miller (Vidora):** 34% is actually quite high for a digital bundle perk in month one, Amara. Usually, platforms hover around 20 to 25% until the second promotional push. So you're definitely doing something right with the placement in the member dashboard.

**[00:02:22] Renee Kowalski (Acme):** Well, Derek’s team put a lot of thought into making sure the benefit was surfaced clearly after members signed up. Though as we know from our broader membership discussions, getting folks to realize they *have* the perk is always half the battle. Derek, remind me, is our current tracking showing any latency issues on the API token handoff when members try to link their Vidora account?

**[00:02:51] Derek Holloway (Acme):** We had a couple of minor timeout blips during the first week of June right after the launch, Marcus, but your engineering team jumped on those quickly. Since about June 8th, the token handoff error rate has been sitting well below 0.1%. Marcus, do you have any updates on your side regarding API stability?

**[00:03:19] Marcus Vance (Vidora):** Yeah, thanks Derek. We traced those initial week-one timeouts to an unexpected spike in concurrent authentication requests from mobile clients right around peak shopping hours. We scaled up our Redis caching layer on June 7th, and since then, p99 latency on the auth endpoint has dropped from 420 milliseconds down to about 85 milliseconds. Everything is green on our status page now.

**[00:03:55] Renee Kowalski (Acme):** That's reassuring. We can't afford any friction in the membership journey, especially since we're leaning so hard on Acme+ retention this fiscal year. Our target is an 86% annual renewal rate, and so far we're pacing a bit ahead at around 87.2%, but perks like this are what keep that engine greased.

**[00:04:22] Greg Miller (Vidora):** That's fantastic to hear. Speaking of keeping things fresh, let’s talk about the upcoming content catalog refresh. As you know, we traditionally rotate our tier-one movie and docuseries bundles at the end of August. We’re planning to drop the fall catalog update on August 25th this year. It includes about 40 new exclusive titles, plus an updated user interface on our player app that reduces clicks to stream from four down to two.

**[00:05:01] Derek Holloway (Acme):** Two clicks is great. Anything that reduces friction on the handoff helps. Will you be providing promotional asset banners for our email marketing and in-app carousel teams by August 10th? Our marketing calendar gets pretty locked down two weeks out, so if we can get assets by then, we can feature the new catalog in the September newsletter.

**[00:05:32] Sarah Chen (Vidora):** Absolutely, Derek. We’ll have the creative asset package—banners, vertical promo tiles, and copy blocks—delivered to your marketing ops shared folder by August 8th, giving you a couple of extra days buffer.

**[00:05:50] Renee Kowalski (Acme):** Perfect. Let’s make sure we Loop in Maya Lindqvist's team or whoever is handling the member portal UI so they know the asset specs match our current layout guidelines. I don't want any layout shifts like what happened with that item page media autoplay experiment over on the US conversion side last month. (Laughs) Different team, I know, but we all share the same frontend design system headaches.

**[00:06:22] Greg Miller (Vidora):** Understood completely, Renee. We’ll adhere strictly to your component guidelines. 

**[00:06:30] Amara Shah (Acme):** Hey Greg, quick technical question on the reporting side—are you guys still pushing the daily batch redemption logs to our S3 bucket by 4:00 AM Eastern? We’ve been running our dbt pipeline transformations in BigQuery at 6:00 AM, and everything has been landing cleanly without missing partitions, but I wanted to double-check if you're planning any schema changes for the August catalog drop that might break our downstream `fact_membership_events` tables.

**[00:07:05] Marcus Vance (Vidora):** No schema changes on the log delivery format, Amara. The JSON payload structure for `benefit_redeemed` events is locked. We’re only updating the content metadata fields inside the catalog feed, not the transaction wrapper. Your pipeline should be completely safe.

**[00:07:28] Amara Shah (Acme):** Excellent, thanks Marcus. That saves me from having to rewrite the parser before my PTO in September.

**[00:07:37] Renee Kowalski (Acme):** PTO in September, Amara? I thought you were covering the MBR prep for Q2 close?

**[00:07:44] Amara Shah (Acme):** Oh, that's not until late September! My trip is the second week. I’ll have all the membership charts locked and loaded well before then.

**[00:07:53] Renee Kowalski (Acme):** (Laughs) Good. Just checking. All right, do we have any other operational blockers on the Vidora integration? Derek, anything else from your side?

**[00:08:08] Derek Holloway (Acme):** No other blockers. The integration is stable, redemption volume is tracking nicely against our expectations following the June 1st launch, and we have the August 25th catalog refresh on our radar with asset delivery locked for August 8th. Everything looks solid.

**[00:08:29] Greg Miller (Vidora):** Perfect. We’ll keep an eye on things on our end as well. Thanks everyone, let’s keep this monthly cadence going. We can set up the agenda for the August sync two weeks prior. Have a great rest of your week!

**[00:08:45] Renee Kowalski (Acme):** Thanks, Greg. Bye everyone.

---
*(Call ended at 12:44 PM ET)*
