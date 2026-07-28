---
title: "Gong call transcript: Acme+ streaming-perk partner transition, Vidora → Reelstream"
source_url: "internal://acme-ecomm/gong/q2fy27__reelstream-partnership-transition-call"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: gong_call
---

**Date:** 2026-05-28  
**Participants:** 
- Renee Kowalski (`renee.kowalski`, SVP Membership, Acme)
- Simone Laurent (`simone.laurent`, Director PM Membership, Acme)
- Derek Holloway (`derek.holloway`, Sr PM Membership Benefits & CLTV, Acme)
- Marcus Vance (Reelstream VP of Partner Success, External Vendor)
- Sarah Chen (Reelstream Technical Integration Lead, External Vendor — *Note: distinct from SaaS entity*)
- Dave Miller (Vidora Account Director, Offboarding Vendor Lead)

---

**[00:00:12] Renee Kowalski:** Morning, everyone. Let’s get started. I know we have a pretty packed agenda today, splitting our time between finalizing the offboarding details with Vidora and running through the technical handover and member communication timeline for the Reelstream onboarding. Today is May 28th, so we are just two business days away from the June 1st hard cutover. Dave, are you on?

**[00:00:41] Dave Miller (Vidora):** Yep, I’m here, Renee. Morning, everyone. We’ve got the final incremental token-revocation batch prepped for midnight on Sunday, June 1st. Existing active sessions will get a graceful redirect banner pointing them to the new Acme member perks portal, but authentication tokens from our side will be fully purged per the data-deletion addendum. 

**[00:01:09] Renee Kowalski:** Excellent. Thanks, Dave. I appreciate all the support since we launched the streaming perk back under Vidora way back on June 1st of last year—hard to believe it's already been a full year since that rollout. But as Derek’s work on the benefit onboarding carousel experiment (`exp_2556`) showed us when it wrapped up last month, member awareness and engagement have shifted a lot since then, and the Reelstream catalog alignment just makes more sense for our retention goals going forward. Dave, we’ll let you and Sarah coordinate on the technical API token handoff offline so we don't eat up the whole hour. 

**[00:02:03] Dave Miller (Vidora):** Sounds good. I will drop off after this section. Good luck with the transition, team.

**[00:02:15] Renee Kowalski:** All right. Marcus, Sarah, welcome to the joint session. Let's pivot to Reelstream readiness. Simone, do you want to walk through the comms and member-facing asset schedule?

**[00:02:30] Simone Laurent:** Sure thing, Renee. So the push notification and email template sequences are locked in Jira. They're scheduled to deploy on Monday morning, June 1st, right at 06:00 ET. We’re keeping the language clean: letting members know their existing Acme+ streaming benefit is getting an upgraded catalog via Reelstream at zero additional cost to their annual or monthly plans. 

**[00:03:01] Derek Holloway:** Yeah, and following up on what Simone said, remember the baseline we found in the benefit adoption data: members using two or more benefits renew at 95% compared to 71% for free-shipping-only folks. And while the streaming bundle historically sits at a 93% renewal rate among users even on its own, only about 34% of our total member base actually knew they had access under Vidora. So the primary goal of this transition isn't just swapping the backend plumbing—it's using the cutover as a marketing hook to drive that awareness past the 34% mark.

**[00:03:45] Marcus Vance (Reelstream):** We’re fully prepped for that traffic spike on our end, Derek. Our CDN caching layers in the US, Canada, and Mexico have been load-tested up to 3x your peak concurrent user count from last Q4. But I do want to make sure we're completely transparent about something: while we know the category-level renewal metric for streaming perks is sitting strong around 93% across your membership base, Reelstream *itself* has only been live as an independent commercial service for about seven weeks as of today—well, technically since early June for other enterprise partners, but our direct enterprise deployment history is still maturing. 

**[00:04:32] Renee Kowalski:** Thanks for reiterating that, Marcus. We noted that in the leadership sync prep: that 93% renewal figure is a category-level read spanning both partner eras—Vidora and now Reelstream—and Reelstream’s specific individual retention and renewal performance isn't independently validated on our cohorts yet. We won't have a clean 12-month cohort lag to evaluate Reelstream's isolated renewal impact until mid-2027. For now, we're tracking short-term activation, streaming app logins within 7 days of signup, and CSAT impact through Medallia.

**[00:05:15] Sarah Chen (Reelstream):** That's fair, Renee. On the technical integration side, our OAuth endpoints are stable in staging. We ran the sandbox synchronization yesterday with Connor Blake's team in Data, and user profile mapping for the 14.6 million true member base checked out with zero drop-offs. The flat BigQuery schema (`nexus-analyst-demo.acme_ecomm.*`) is receiving our daily event pings cleanly—no nested path issues like what happened with the `member_cltv` mart audit back in Q1.

**[00:05:58] Simone Laurent:** Quick administrative question on that—are we still seeing any latency on the benefit redemption event logs in `fact_membership_events`? Connor mentioned during Tuesday's data sync that the Airflow retry logic occasionally backs up the mart refreshes if upstream table locks happen during peak traffic.

**[00:06:22] Sarah Chen (Reelstream):** We’ve implemented an asynchronous queue on our webhook publisher specifically to prevent locking your ingestion pipelines. Even if your internal Airflow DAG stalls for a few hours, our side buffers up to 72 hours of events and replays them in order once the endpoint acknowledges.

**[00:06:48] Renee Kowalski:** That’s a relief. We don't want a repeat of what happened with the marketplace summary mart back in June '25 when things ran 14 hours stale. 

**[00:07:01] Derek Holloway:** Agreed. Just to circle back on the member communication plan, Simone—are we doing any special segmentation for the dormant cohort? Remember Marisol (`mem_1000178`), our classic example of the `member_cltv` join trap who's paying annual but hasn't ordered in 12 months? Do they get the Reelstream announcement, or do we suppress them so we don't trigger unnecessary churn tickets?

**[00:07:34] Simone Laurent:** We’re including them in the general benefit broadcast. The logic is that a fresh, high-value perk like Reelstream might actually reactivate a dormant user who hasn't engaged with physical eCommerce in a while, without us having to route them through Care. Speaking of Care, has Aisha or Dominic flagged any anticipated deflection impacts for the first week of June?

**[00:08:02] Renee Kowalski:** Aisha Rahman hasn't raised any red flags. Since they partially shipped the Bot Handoff Threshold experiment (`exp_2489`) back in May for non-billing categories—which got us that +3pp bump in deflection while keeping CSAT stable—the bot is handling routine benefit inquiries much cleaner than it did during the Ask Acme v2 launch last fall. If a member doesn't know how to activate their Reelstream account, the bot should deflect it automatically without them needing to queue for live chat.

**[00:08:42] Marcus Vance (Reelstream):** Perfect. We’ll have a dedicated 24/7 technical escalation bridge staffed on our side from June 1st through June 7th just in case there are any single sign-on (SSO) hiccups during the initial rush. Acme can pipe those straight to our tier-2 support desk via the shared Slack channel.

**[00:09:05] Renee Kowalski:** Excellent. Thanks, Marcus. Let's lock in the calendar invites for our daily 15-minute standups during launch week (June 1–5) so we can monitor activation rates and support ticket volume in real time. Simone, please send those out to the core membership and data teams. If there's nothing else on the technical or operational side, we'll call it a wrap. Thanks, everyone.

---
