---
title: "Gong expansion call — cust_000089 Pro → Business upgrade"
source_url: "internal://acme/gong/expansion/cust000089"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). AE: Sarah Lopez."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong expansion call — cust_000089 Pro → Business upgrade

**Call Date**: 2026-04-22
**Participants**:
*   **Sarah Lopez** (Acme Account Executive)
*   **Jordan Vance** (Director of Ops, Silverline Logistics — `cust_000089`)
*   **Maya Gupta** (Engineering Lead, Silverline Logistics — `cust_000089`)

**Context**: Silverline Logistics (`cust_000089`) has been on the Pro plan since Q3 2024. They appeared on the "Quota Breach Risk" pitch list after `marts/product/workflow_runs_daily.sql` showed them hitting >90% of their 10,000 run quota for January, February, and March 2026.

---

00:00 **Sarah Lopez**: Hey Jordan, Maya. Great to see you both again. How’s the new warehouse automation project coming along?

00:05 **Jordan Vance**: It’s moving fast, Sarah. A little too fast, maybe. That’s actually why we’re on the phone today. Maya’s team is spinning up more workflows than we originally anticipated.

00:12 **Sarah Lopez**: I noticed that in our usage alerts. I was looking at your daily run counts—you guys hit about 9,200 runs last month, and you’re already on track to clear 9,500 for April. You’re right up against that 10k Pro ceiling.

00:25 **Maya Gupta**: Yeah, we’ve had to throttle a few of the non-critical inventory syncs just to make sure the shipping label generator doesn't hit the limit and die mid-day. It’s not a sustainable way for us to operate. We’re also looking at adding about 6 more people from the logistics team as 'Builders' this month.

00:40 **Sarah Lopez**: That makes total sense. Throttling is exactly what we want to avoid. Given the seat growth and the run volume, it’s definitely time to talk about moving Silverline up to the Business tier.

00:52 **Jordan Vance**: We looked at the pricing page. It’s a jump, right? $49 to $149 per seat? And I saw there's a 50-seat minimum? We're only at 18 seats right now, even with the 6 Maya is adding.

01:05 **Sarah Lopez**: So, the 50-seat minimum is the standard for Business, but I’ve been talking to my VP, Marcus Webb, about your account specifically. Because you’ve been such a power user on Pro, I have some flexibility to bridge that gap. But before we get into the numbers, I want to make sure the features actually solve your bottlenecks.

01:20 **Maya Gupta**: The run quota is the big one—moving from 10k to 100k runs a month gives us a lot of breathing room. But I’m also interested in the SSO and the audit logs. We’re starting our SOC2 prep and our auditor is already asking how we manage access to these workflows.

01:35 **Sarah Lopez**: Business includes full SAML SSO and 90-day audit logs. You can see exactly who changed a step in a workflow and when. It’s a requirement for almost all our SOC2 customers. You also get priority support, so if a shipping label workflow does go down, you’re at the front of the queue.

01:55 **Jordan Vance**: Okay, that hits the requirements. Let's talk about the "bridge" you mentioned. We can't pay for 50 seats when we're using 24.

02:10 **Sarah Lopez**: Here’s what I can do. I can get you onto the Business tier with a 30-seat floor instead of 50. That covers your current 18, the 6 Maya is adding, and gives you 6 more for growth. We’d move the unit price to the standard $149, but I can apply a 10% discount for the first year if we move to an annual billing cycle.

02:30 **Jordan Vance**: We’re currently monthly on the credit card. Annual is a bit of a hurdle for procurement, but for 10% off the $149, I can probably push it through. What does that do to the total?

02:45 **Sarah Lopez**: At 30 seats, with the 10% discount on an annual commitment, you’re looking at $48,276 for the year. That’s roughly $4,023 a month. You’re currently paying about $882 a month on Pro for 18 seats. So it’s an increase, but it removes the run limits entirely for your current scale and checks the SOC2 boxes.

03:10 **Maya Gupta**: Does that include the new integrations? We need the Snowflake connector for the data team.

03:15 **Sarah Lopez**: All integrations are included in Business, including the premium ones like Snowflake and NetSuite. No extra fees there.

03:25 **Jordan Vance**: If we hit 31 seats, what happens?

03:30 **Sarah Lopez**: You just add them pro-rata. We’ll true it up on the next invoice. And per our `notion__pricing-tiers.md` policy, if you stay above 80% utilization on those 30 seats, we can talk about further volume discounts down the road.

03:45 **Jordan Vance**: Send over the proposal. I need to show the CFO why we’re 4x-ing our spend on Acme, but the "SOC2 compliance" and "unblocking the warehouse" angles should work.

04:00 **Sarah Lopez**: I’ll get the DocuSign over by EOD. I’ll also include the technical spec for the SSO setup so Maya can look it over. If we get this signed by Friday, I can have the quota lifted before your Monday morning run spike.

04:15 **Maya Gupta**: That would be huge. Thanks, Sarah.

04:20 **Sarah Lopez**: Thanks both. Talk soon.
