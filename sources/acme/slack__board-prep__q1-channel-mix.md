---
title: "Slack #board-prep — Q1 2026 channel mix slide"
source_url: "internal://acme/slack/board-prep/q1-channel-mix"
license: "synthetic-demo"
attribution: "Acme Inc Slack archives (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #board-prep

**2026-04-08 09:12 AM**
**@lina.cho**: @jorge.martinez Hey Jorge, I’m pulling the "New Logos by Channel" slide for the Q1 board deck. Can you give me the final count of new paid logos for Q1 2026 broken down by acquisition channel? Need to make sure I’m aligned with the `bookings_attribution` mart before I lock the slide.

**2026-04-08 09:45 AM**
**@jorge.martinez**: Hey Lina, just ran the query against `marts/sales/bookings_attribution`. Here is the Q1 breakdown for new paid logos:
- **Outbound**: 42
- **Paid Search**: 28
- **Organic**: 18
- **Content**: 14
- **Referral**: 12
- **Partner**: 8
Total: 122 new logos.

**2026-04-08 09:47 AM**
**@jorge.martinez**: ⚠️ One big caveat for the slide: the **Partner** count looks low compared to Q4, but that’s because we changed the tagging logic mid-Q1 (see `dbt__model__bookings_attribution.md`). We used to bucket some "referral" leads as "partner" if they came from a co-marketing webinar, but now they stay in "referral" unless there's a registered partner ID. Q4-vs-Q1 is apples-to-oranges for those two buckets.

**2026-04-08 10:02 AM**
**@lina.cho**: Got it. I'll add a footnote about the tagging change so Rachel doesn't ask why partner-led growth looks like it's stalling. 

**2026-04-08 10:05 AM**
**@lina.cho**: Do you have the average sales cycle (days to close) for these? I want to show the efficiency of the paid vs. outbound motion.

**2026-04-08 10:14 AM**
**@jorge.martinez**: Yep, pulled from the `sales_cycle_days` column:
- **Outbound**: 73 days
- **Paid Search**: 58 days
- **Partner**: 41 days
Outbound is still our longest drag, but the ACV is higher there. Paid search is surprisingly efficient this quarter.

**2026-04-08 10:16 AM**
**@jasmine.park**: @jorge.martinez @lina.cho Jumping in here — the Paid Search efficiency is likely due to the new "Enterprise Workflow" campaign we ran in Feb. It's hitting high-intent keywords. 

**2026-04-08 10:18 AM**
**@jasmine.park**: Do we have the LTV breakdown for these yet? I'm trying to defend the Q2 search budget and showing that Paid Search has better LTV/CAC than Outbound would be huge.

**2026-04-08 10:25 AM**
**@lina.cho**: @jasmine.park I'm looking at the `post_close_mrr_delta_vs_initial_usd` in the attribution mart. Outbound actually has better expansion rates so far (more seats added in month 3), which usually leads to higher LTV. Paid search logos tend to stay flat for the first 6 months.

**2026-04-08 10:30 AM**
**@marcus.webb**: @lina.cho @jorge.martinez The Outbound sales cycle being 73 days is actually an improvement from Q4 (was 81). The SDR team is doing a better job qualifying before handing off to AEs. I'd highlight that on the slide.

**2026-04-08 10:35 AM**
**@jorge.martinez**: Good catch @marcus.webb. I'll update the `bookings_attribution` documentation to note the Q1 SDR process change as a factor in the cycle reduction.

**2026-04-08 10:42 AM**
**@lina.cho**: Perfect. I'll draft the slide with these numbers and the partner footnote. @jorge.martinez can you double-check the "Referral" LTV? It looks like we had one massive Enterprise referral in Q1 that might be skewing the average.

**2026-04-08 10:45 AM**
**@jorge.martinez**: Correct, that was `cust_000512` (Vandelay Industries). $120k ACV referral. If you strip that out, Referral LTV is actually lower than Organic. I'll send you the "median" view for the slide. 👍

**2026-04-08 10:46 AM**
**@lina.cho**: Thanks! 🚀
